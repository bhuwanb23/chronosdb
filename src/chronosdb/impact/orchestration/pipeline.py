from __future__ import annotations

from datetime import UTC, datetime

from ..contracts.enums import DataQualityStatus, ImpactStatus
from ..contracts.errors import ContractError
from ..contracts.requests import SimulationHorizon
from ..contracts.results import ImpactResult, canonical_hash
from ..disruption.supplier_outage import Disruption, resolve_purchase_order_impacts
from ..disruption.validation import validate_disruption
from ..rules.versions import RuleSet
from ..state.reconstruction import OperationalState
from ..state.validation import insufficient_record_sets
from ..supply.projection import project_receipts


def _utc_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def calculate_impact(
    state: OperationalState,
    disruption: Disruption,
    horizon: SimulationHorizon,
    rules: RuleSet,
    scenario_id: str = "UNKNOWN",
) -> ImpactResult:
    """Calculate the deterministic 5A–5G supply-impact slice."""
    if horizon.as_of_time.tzinfo is None or horizon.simulation_end_time.tzinfo is None:
        raise ContractError("simulation horizon timestamps must include timezone")
    if _utc_timestamp(horizon.as_of_time) != state.identity.as_of_time:
        raise ContractError("state as_of_time must equal simulation horizon as_of_time")
    validate_disruption(disruption)
    insufficient = insufficient_record_sets(state.records)
    impacts = resolve_purchase_order_impacts(state, disruption) if not insufficient else ()
    receipts = project_receipts(impacts, horizon) if not insufficient else ()
    affected_components = sorted({impact.component_id for impact in impacts})
    provenance = {
        "state_version": state.identity.state_version,
        "input_state_hash": state.identity.state_hash,
        "rule_set_version": rules.version,
        "rule_ids": [
            "STATE-001",
            "STATE-002",
            "DQ-001",
            "SUP-001",
            "SUP-004",
            "SUP-005",
            "SUP-006",
        ],
        "source_record_ids": sorted(
            {disruption.event_id}
            | {source_id for impact in impacts for source_id in impact.source_record_ids}
        ),
    }
    run_fingerprint = canonical_hash(
        {
            "state": state.identity.state_hash,
            "scenario_id": scenario_id,
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
    data_quality_status = (
        DataQualityStatus.INSUFFICIENT
        if insufficient
        else DataQualityStatus.PARTIAL
        if state.warnings
        else DataQualityStatus.COMPLETE
    )
    errors = [f"insufficient required state: {', '.join(insufficient)}"] if insufficient else []
    result = ImpactResult(
        impact_run_id=f"IR-{run_fingerprint[:16]}",
        scenario_id=scenario_id,
        status=ImpactStatus.REJECTED if insufficient else ImpactStatus.PARTIALLY_COMPLETED,
        data_quality_status=data_quality_status,
        rule_set_version=rules.version,
        input_state_hash=state.identity.state_hash,
        affected_purchase_orders=[impact.to_dict() for impact in impacts],
        affected_components=affected_components,
        inventory_timelines=[receipt.to_dict() for receipt in receipts],
        warnings=["Downstream inventory, production, fulfilment, and financial stages are 5H–5M."],
        errors=errors,
        provenance=provenance,
    )
    result.result_hash = result.to_dict()["result_hash"]
    return result
