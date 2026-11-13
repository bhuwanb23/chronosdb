from __future__ import annotations

from contextlib import nullcontext
from datetime import UTC, datetime
from typing import Any

from ..causality.builder import build_causal_traces
from ..contracts.enums import DataQualityStatus, ImpactStatus
from ..contracts.errors import ContractError
from ..contracts.requests import SimulationHorizon
from ..contracts.results import ImpactResult, canonical_hash
from ..disruption.supplier_outage import Disruption, resolve_purchase_order_impacts
from ..disruption.validation import validate_disruption
from ..fulfilment.allocation import build_customer_fulfilment
from ..fulfilment.sla import calculate_sla_and_financial_impact
from ..inventory import InventoryEvent, build_inventory_timelines, detect_shortages
from ..materials import allocate_materials, build_material_requirements
from ..observability import ImpactDiagnostics
from ..persistence.repository import ExecutionLedger
from ..production import schedule_production
from ..provenance.calculation_trace import metric_provenance
from ..rules.versions import RuleSet
from ..state.reconstruction import OperationalState
from ..state.validation import insufficient_record_sets
from ..supply.projection import project_receipts
from ..validation.data_quality import QualityIssue, QualitySeverity, classify_issues


def _utc_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _diagnostic_stage(
    diagnostics: ImpactDiagnostics | None,
    name: str,
) -> Any:
    return diagnostics.stage(name) if diagnostics is not None else nullcontext()


def calculate_impact(
    state: OperationalState,
    disruption: Disruption,
    horizon: SimulationHorizon,
    rules: RuleSet,
    scenario_id: str = "UNKNOWN",
    allocation_policy: str = "priority-due-date-v1",
    scheduling_policy: str = "batch-capacity-v1",
    ledger: ExecutionLedger | None = None,
    diagnostics: ImpactDiagnostics | None = None,
) -> ImpactResult:
    """Calculate the deterministic do-nothing impact through Phase 5Q."""
    if allocation_policy not in {"priority-due-date-v1", "fifo-v1"}:
        raise ContractError(f"unsupported allocation policy: {allocation_policy}")
    if scheduling_policy not in {"batch-capacity-v1"}:
        raise ContractError(f"unsupported scheduling policy: {scheduling_policy}")
    if horizon.as_of_time.tzinfo is None or horizon.simulation_end_time.tzinfo is None:
        raise ContractError("simulation horizon timestamps must include timezone")
    if _utc_timestamp(horizon.as_of_time) != state.identity.as_of_time:
        raise ContractError("state as_of_time must equal simulation horizon as_of_time")
    validate_disruption(disruption)
    insufficient = insufficient_record_sets(state.records)
    with _diagnostic_stage(diagnostics, "disruption_resolution"):
        impacts = resolve_purchase_order_impacts(state, disruption) if not insufficient else ()
    with _diagnostic_stage(diagnostics, "supply_projection"):
        receipts = project_receipts(impacts, horizon) if not insufficient else ()
    affected_components = sorted({impact.component_id for impact in impacts})
    scenario_payload = next(
        (
            scenario
            for scenario in state.scenario_inputs
            if scenario.get("scenario_id") == scenario_id
        ),
        None,
    )
    run_fingerprint = canonical_hash(
        {
            "state": state.identity.state_hash,
            "scenario_id": scenario_id,
            "scenario_input": scenario_payload,
            "allocation_policy": allocation_policy,
            "scheduling_policy": scheduling_policy,
            "disruption": {
                "event_id": disruption.event_id,
                "event_type": disruption.event_type,
                "supplier_id": disruption.supplier_id,
                "start_time": _utc_timestamp(disruption.start_time),
                "end_time": _utc_timestamp(disruption.end_time),
                "recovery_lag_seconds": disruption.recovery_lag.total_seconds(),
                "scope_type": disruption.scope_type,
                "component_ids": sorted(disruption.component_ids),
                "purchase_order_ids": sorted(disruption.purchase_order_ids),
            },
            "horizon": {
                "as_of_time": _utc_timestamp(horizon.as_of_time),
                "simulation_end_time": _utc_timestamp(horizon.simulation_end_time),
            },
            "rules": {
                "version": rules.version,
                "domain_model_version": rules.domain_model_version,
                "dataset_compatibility": list(rules.dataset_compatibility),
                "definitions": [rule.__dict__ for rule in rules.rules],
            },
        }
    )
    impact_run_id = f"IR-{run_fingerprint[:16]}"
    if diagnostics is not None:
        diagnostics.start(impact_run_id)
        diagnostics.count("purchase_orders_affected", len(impacts))
        diagnostics.count("receipt_events_changed", len(receipts))
    data_quality_status = (
        DataQualityStatus.INSUFFICIENT
        if insufficient
        else DataQualityStatus.PARTIAL
        if state.warnings
        else DataQualityStatus.COMPLETE
    )
    errors = [f"insufficient required state: {', '.join(insufficient)}"] if insufficient else []
    if insufficient:
        if diagnostics is not None:
            diagnostics.errors = len(errors)
            diagnostics.finish(ImpactStatus.REJECTED.value)
        result = ImpactResult(
            impact_run_id=impact_run_id,
            scenario_id=scenario_id,
            status=ImpactStatus.REJECTED,
            data_quality_status=data_quality_status,
            rule_set_version=rules.version,
            input_state_hash=state.identity.state_hash,
            affected_purchase_orders=[],
            affected_components=[],
            warnings=list(state.warnings),
            errors=errors,
            provenance={
                "state_version": state.identity.state_version,
                "input_state_hash": state.identity.state_hash,
                "rule_set_version": rules.version,
                "source_record_ids": [disruption.event_id],
            },
        )
        result.result_hash = result.to_dict()["result_hash"]
        return result
    if ledger is not None:
        existing = ledger.find_by_fingerprint(run_fingerprint)
        if existing is not None and existing.payload:
            return ImpactResult.from_dict(existing.payload)
        ledger.begin(
            impact_run_id=f"IR-{run_fingerprint[:16]}",
            scenario_id=scenario_id,
            request_fingerprint=run_fingerprint,
            input_state_hash=state.identity.state_hash,
            rule_set_version=rules.version,
            data_quality_status=data_quality_status.value,
        )
    with _diagnostic_stage(diagnostics, "inventory_projection"):
        timelines = build_inventory_timelines(state, horizon, receipts)
    if diagnostics is not None:
        diagnostics.count("inventory_timelines_processed", len(timelines))
    scenario_order_ids: set[str] | None = None
    scenario_line_ids: set[str] | None = None
    if scenario_payload is not None:
        order_ids = {
            str(order.get("production_order_id"))
            for order in scenario_payload.get("orders", [])
            if order.get("production_order_id")
        }
        if order_ids:
            scenario_order_ids = order_ids
        line_ids = {
            str(line.get("id"))
            for line in scenario_payload.get("customer_order_lines", [])
            if line.get("id")
        }
        if line_ids:
            scenario_line_ids = line_ids
    requirements = build_material_requirements(
        state,
        horizon.as_of_time,
        horizon.simulation_end_time,
        component_ids=None,
        production_order_ids=scenario_order_ids,
    )
    baseline_components = {
        requirement.component_id for requirement in requirements
    } - set(affected_components)
    with _diagnostic_stage(diagnostics, "material_allocation"):
        allocations = allocate_materials(
            requirements,
            timelines,
            policy=allocation_policy,
            baseline_component_ids=baseline_components,
        )
    shortages = detect_shortages(allocations, horizon.simulation_end_time)
    with _diagnostic_stage(diagnostics, "production_scheduling"):
        production_impacts = schedule_production(
            state,
            requirements,
            allocations,
            horizon,
            policy=scheduling_policy,
        )
    if diagnostics is not None:
        diagnostics.count("shortages_found", len(shortages))
        diagnostics.count(
            "production_batches_scheduled",
            sum(len(impact.batches) for impact in production_impacts),
        )
    projected_starts = {
        batch.batch_id: batch
        for impact in production_impacts
        for batch in impact.batches
        if batch.projected_start is not None
    }
    projected_consumption_events: list[InventoryEvent] = []
    for allocation in allocations:
        batch = projected_starts.get(allocation.batch_id)
        if batch is None or allocation.component_id not in affected_components:
            continue
        if batch.projected_start is None:
            continue
        projected_consumption_events.append(
            InventoryEvent(
                event_id=f"ISSUE-{allocation.batch_id}-{allocation.component_id}",
                event_time=batch.projected_start,
                event_type="PROJECTED_CONSUMPTION",
                warehouse_id=allocation.warehouse_id,
                component_id=allocation.component_id,
                quantity=allocation.required_quantity,
                reference_id=batch.production_order_id,
                source_record_ids=(allocation.batch_id, batch.production_order_id),
            )
        )
    projected_consumption = tuple(projected_consumption_events)
    with _diagnostic_stage(diagnostics, "inventory_projection"):
        timelines = build_inventory_timelines(
            state,
            horizon,
            receipts,
            projected_consumption=projected_consumption,
        )
    if diagnostics is not None:
        diagnostics.count("inventory_timelines_processed", len(timelines))
    first_shortage_by_key: dict[tuple[str, str], datetime] = {}
    for shortage in shortages:
        key = (shortage.warehouse_id, shortage.component_id)
        current = first_shortage_by_key.get(key)
        if current is None or shortage.required_time < current:
            first_shortage_by_key[key] = shortage.required_time
    timelines = tuple(
        timeline.with_shortage_time(
            first_shortage_by_key.get((timeline.warehouse_id, timeline.component_id))
        )
        for timeline in timelines
    )
    with _diagnostic_stage(diagnostics, "customer_impact"):
        customer_impacts = build_customer_fulfilment(
            state,
            production_impacts,
            horizon,
            production_order_ids=scenario_order_ids,
            customer_order_line_ids=scenario_line_ids,
        )
        sla_results, headline_metrics = calculate_sla_and_financial_impact(
            customer_impacts,
            disruption_caused_production_order_ids={
                shortage.production_order_id for shortage in shortages
            },
            horizon_end=horizon.simulation_end_time,
        )
    if diagnostics is not None:
        diagnostics.count("customer_lines_calculated", len(sla_results))
    quality_issues = [
        QualityIssue(
            code="MISSING_PROMISED_DELIVERY",
            severity=QualitySeverity.CRITICAL_FOR_ENTITY,
            entity_type="CUSTOMER_ORDER_LINE",
            entity_id=item.customer_order_line_id,
            message="Promised delivery is required for SLA calculation.",
            affected_outputs=("sla_status", "delay_hours", "revenue_at_risk"),
        )
        for item in sla_results
        if item.status == "INSUFFICIENT_DATA"
    ]
    quality_status = classify_issues(quality_issues)
    if state.warnings and quality_status == DataQualityStatus.COMPLETE:
        quality_status = DataQualityStatus.PARTIAL_NONCRITICAL
    data_quality_status = quality_status
    headline_metrics["affected_supplier_count"] = len({item.supplier_id for item in impacts})
    headline_metrics["affected_purchase_order_count"] = len(impacts)
    headline_metrics["supply_affected_component_count"] = len(affected_components)
    headline_metrics["shortage_affected_component_count"] = len(
        {shortage.component_id for shortage in shortages}
    )
    with _diagnostic_stage(diagnostics, "causal_trace_build"):
        traces = build_causal_traces(
            disruption,
            impacts,
            production_impacts,
            sla_results,
            state.identity,
            rules.version,
        )
    if diagnostics is not None:
        diagnostics.count("causal_nodes_generated", sum(len(trace.nodes) for trace in traces))
    provenance = {
        "state_version": state.identity.state_version,
        "input_state_hash": state.identity.state_hash,
        "rule_set_version": rules.version,
        "allocation_policy": allocation_policy,
        "scheduling_policy": scheduling_policy,
        "scenario_input_hash": canonical_hash(scenario_payload)
        if scenario_payload is not None
        else None,
        "rule_ids": [
            "STATE-001",
            "STATE-002",
            "DQ-001",
            "SUP-001",
            "SUP-004",
            "SUP-005",
            "SUP-006",
            "INV-004",
            "ALLOC-001",
            "INV-003",
            "PROD-003",
            "FUL-001",
            "SLA-001",
            "FIN-004",
            "CAU-001",
        ],
        "source_record_ids": sorted(
            {disruption.event_id}
            | {source_id for impact in impacts for source_id in impact.source_record_ids}
        ),
        "projected_receipts": [receipt.to_dict() for receipt in receipts],
        "material_requirements": [requirement.to_dict() for requirement in requirements],
        "material_allocations": [allocation.to_dict() for allocation in allocations],
        "metric_provenance": {
            "revenue_at_risk": metric_provenance(
                "METRIC-REVENUE-AT-RISK",
                "revenue_at_risk",
                headline_metrics["revenue_at_risk"],
                "INR",
                "FIN-004",
                rules.version,
                [item.customer_order_line_id for item in sla_results],
                ["FIN-004"],
                scenario_id,
                impact_run_id,
                state.identity.state_hash,
                horizon.as_of_time,
                data_quality_status.value,
            ),
            "total_delay_unit_hours": metric_provenance(
                "METRIC-DELAY-UNIT-HOURS",
                "total_delay_unit_hours",
                headline_metrics["total_delay_unit_hours"],
                "quantity-hours",
                "SLA-001",
                rules.version,
                [item.customer_order_line_id for item in sla_results],
                ["SLA-001"],
                scenario_id,
                impact_run_id,
                state.identity.state_hash,
                horizon.as_of_time,
                data_quality_status.value,
            ),
        },
        "causal_trace_ids": [trace.trace_id for trace in traces],
        "quality_issues": [issue.to_dict() for issue in quality_issues],
    }
    result = ImpactResult(
        impact_run_id=impact_run_id,
        scenario_id=scenario_id,
        status=(
            ImpactStatus.COMPLETED
            if data_quality_status == DataQualityStatus.COMPLETE
            else ImpactStatus.PARTIALLY_COMPLETED
        ),
        data_quality_status=data_quality_status,
        rule_set_version=rules.version,
        input_state_hash=state.identity.state_hash,
        affected_purchase_orders=[impact.to_dict() for impact in impacts],
        affected_components=affected_components,
        inventory_timelines=[
            timeline.to_dict()
            for timeline in timelines
            if timeline.component_id in affected_components
        ],
        shortages=[shortage.to_dict() for shortage in shortages],
        affected_production_orders=[
            impact.to_dict() for impact in production_impacts if impact.delay_hours > 0
        ],
        affected_customer_orders=[
            item.to_dict() for item in sla_results if item.status == "BREACHED"
        ],
        headline_metrics=headline_metrics,
        causal_traces=[trace.to_dict() for trace in traces],
        warnings=list(state.warnings),
        errors=errors
        + [f"{issue.code}: {issue.message}" for issue in quality_issues],
        provenance=provenance,
    )
    result.result_hash = result.to_dict()["result_hash"]
    if ledger is not None:
        with _diagnostic_stage(diagnostics, "persistence"):
            try:
                ledger.complete(
                    impact_run_id,
                    status=result.status.value,
                    data_quality_status=result.data_quality_status.value,
                    result_hash=result.result_hash,
                    payload=result.to_dict(),
                )
            except Exception as exc:
                if diagnostics is not None:
                    diagnostics.errors += 1
                ledger.fail(impact_run_id, error_summary=str(exc))
                raise
    if diagnostics is not None:
        diagnostics.warnings = len(result.warnings)
        diagnostics.errors = len(result.errors)
        diagnostics.finish(result.status.value)
    return result
