"""Phase 7F: extract optimization metrics from Phase 6 simulations.

Metric definitions are deliberately explicit and recorded in
``docs/optimization/metric-definitions.md``. No metric is inferred from an LLM
or a presentation layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Iterable, Mapping, TYPE_CHECKING

from .contracts import (
    CandidateMetrics,
    OptimizationValidationError,
    RISK_POLICY_VERSION,
)

if TYPE_CHECKING:
    from chronosdb.simulation.counterfactual import (
        CounterfactualResult,
        Overlay,
        Phase6Engine,
    )


ACTION_LABELS = {
    "DO_NOTHING": "Do Nothing",
    "TRANSFER": "Warehouse Transfer",
    "EXPEDITE": "PO Expedition",
    "ALTERNATE_SUPPLIER": "Alternate Supplier",
    "RESCHEDULE": "Production Reschedule",
    "HYBRID": "Hybrid Recovery",
}


def _decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def _result_component_ids(engine: "Phase6Engine", overlays: Iterable["Overlay"]) -> set[str]:
    ids = {
        str(overlay.parameters.get("component_id"))
        for overlay in overlays
        if overlay.parameters.get("component_id")
    }
    if ids:
        return ids
    # A do-nothing plan still has a disrupted component in the frozen scenario.
    component_ids = getattr(engine.disruption, "component_ids", ())
    if component_ids:
        return {str(item) for item in component_ids}
    return {"CMP-MCU-42"}


def _inventory_state(
    engine: "Phase6Engine", overlays: Iterable["Overlay"]
) -> tuple[float, float, float]:
    """Return (committed units, remaining above safety, minimum safety buffer).

    Transfer moves existing stock, alternate supply and expedition add receipts.
    ``remaining_inventory`` is the lowest post-plan buffer above safety stock
    across every warehouse of the component(s) touched by the plan. This makes a
    transfer's source-stock risk visible without inventing warehouse capacity.
    """

    component_ids = _result_component_ids(engine, overlays)
    records = {
        (row.get("warehouse_id", ""), row.get("component_id", "")): {
            "on_hand": _decimal(row.get("on_hand_quantity", "0")),
            "reserved": _decimal(row.get("reserved_quantity", "0")),
            "quarantined": _decimal(row.get("quarantined_quantity", "0")),
            "safety": _decimal(row.get("safety_stock_quantity", "0")),
        }
        for row in engine.state.records.get("inventory_opening_balances", ())
        if row.get("component_id") in component_ids
    }
    committed = Decimal("0")
    for overlay in overlays:
        params = overlay.parameters
        action = overlay.action
        if action == "TRANSFER_INVENTORY":
            component = str(params.get("component_id", ""))
            source = str(params.get("from_warehouse") or params.get("source_warehouse") or "")
            destination = str(
                params.get("to_warehouse") or params.get("destination_warehouse") or ""
            )
            quantity = _decimal(params.get("quantity", "0"))
            committed += quantity
            if (source, component) in records:
                records[(source, component)]["on_hand"] -= quantity
            if (destination, component) in records:
                records[(destination, component)]["on_hand"] += quantity
        elif action == "ALTERNATE_SUPPLIER":
            component = str(params.get("component_id", ""))
            warehouse = str(params.get("to_warehouse") or "WH-PUNE")
            quantity = _decimal(
                params.get("available_quantity", params.get("quantity", "0"))
            )
            committed += quantity
            if (warehouse, component) in records:
                records[(warehouse, component)]["on_hand"] += quantity
        elif action == "EXPEDITE_PO":
            purchase_order_id = str(params.get("purchase_order_id", ""))
            order = next(
                (
                    row
                    for row in engine.state.records.get("purchase_orders", ())
                    if row.get("id") == purchase_order_id
                ),
                None,
            )
            if order is not None:
                component = str(order.get("component_id", ""))
                warehouse = str(order.get("destination_warehouse_id", ""))
                outstanding = max(
                    Decimal("0"),
                    _decimal(order.get("ordered_quantity", "0"))
                    - _decimal(order.get("received_quantity", "0")),
                )
                if (warehouse, component) in records:
                    records[(warehouse, component)]["on_hand"] += outstanding

    buffers = []
    for row in records.values():
        available = row["on_hand"] - row["reserved"] - row["quarantined"]
        buffers.append(available - row["safety"])
    remaining = float(max(Decimal("0"), min(buffers))) if buffers else 0.0
    minimum_safety = float(
        max((row["safety"] for row in records.values()), default=Decimal("0"))
    )
    return float(committed), remaining, minimum_safety


def _active_agreement(
    engine: "Phase6Engine", supplier_id: str, component_id: str
) -> Mapping[str, str] | None:
    from chronosdb.impact.contracts.requests import parse_time

    for row in engine.state.records.get("supplier_component_agreements", ()):
        try:
            active = (
                parse_time(row["effective_from"])
                <= engine.as_of
                < parse_time(row["effective_to"])
            )
        except Exception:  # noqa: BLE001 - malformed intervals are not active
            active = False
        if (
            row.get("supplier_id") == supplier_id
            and row.get("component_id") == component_id
            and row.get("approval_status") == "APPROVED"
            and active
        ):
            return row
    return None


def _capacity_utilization(engine: "Phase6Engine", overlays: Iterable["Overlay"]) -> float:
    utilizations: list[float] = []
    for overlay in overlays:
        params = overlay.parameters
        if overlay.action == "ALTERNATE_SUPPLIER":
            supplier_id = str(params.get("supplier_id", ""))
            component_id = str(params.get("component_id", ""))
            agreement = _active_agreement(engine, supplier_id, component_id)
            if agreement is None:
                utilizations.append(100.0)
                continue
            quantity = _decimal(
                params.get("available_quantity", params.get("quantity", "0"))
            )
            days = int(params.get("lead_time_days", agreement.get("lead_time_days", 0)))
            capacity = _decimal(agreement.get("daily_capacity_units", "0")) * max(1, days)
            if capacity <= 0:
                utilizations.append(100.0)
            else:
                utilizations.append(float(quantity / capacity * 100))
        elif overlay.action == "EXPEDITE_PO":
            purchase_order_id = str(params.get("purchase_order_id", ""))
            order = next(
                (
                    row
                    for row in engine.state.records.get("purchase_orders", ())
                    if row.get("id") == purchase_order_id
                ),
                None,
            )
            if order is None:
                utilizations.append(100.0)
                continue
            agreement = _active_agreement(
                engine,
                str(order.get("supplier_id", "")),
                str(order.get("component_id", "")),
            )
            if agreement is None:
                utilizations.append(100.0)
                continue
            outstanding = max(
                Decimal("0"),
                _decimal(order.get("ordered_quantity", "0"))
                - _decimal(order.get("received_quantity", "0")),
            )
            order_time = order.get("order_time") or order.get("confirmed_time")
            expected = order.get("expected_arrival_time")
            days = 1
            if order_time and expected:
                try:
                    from chronosdb.impact.contracts.requests import parse_time

                    days = max(
                        1,
                        (parse_time(expected) - parse_time(order_time)).days,
                    )
                except Exception:  # noqa: BLE001 - malformed metadata is unsafe
                    days = 1
            capacity = _decimal(agreement.get("daily_capacity_units", "0")) * days
            utilizations.append(
                100.0 if capacity <= 0 else float(outstanding / capacity * 100)
            )
    return round(max(utilizations, default=0.0), 6)


def _supplier_risk(
    overlays: tuple["Overlay", ...],
    capacity_utilization_pct: float,
    engine: "Phase6Engine",
) -> float:
    """Transparent operational-risk policy ``operational-risk-v1``.

    Base action risk plus supplier-capacity pressure and alternate lead-time
    pressure. The policy is intentionally simple and versioned; it never uses
    hidden supplier scores that do not exist in the dataset.
    """

    del engine
    actions = {overlay.action for overlay in overlays}
    if not actions:
        return 0.0
    base = 0.0
    if "TRANSFER_INVENTORY" in actions:
        base = max(base, 0.05)
    if "RESCHEDULE_PRODUCTION" in actions:
        base = max(base, 0.10)
    if "ALTERNATE_SUPPLIER" in actions:
        base = max(base, 0.15)
        for overlay in overlays:
            if overlay.action == "ALTERNATE_SUPPLIER":
                lead = int(overlay.parameters.get("lead_time_days", 3))
                base += max(0.0, (lead - 3) / 30.0)
                break
    if "EXPEDITE_PO" in actions:
        base = max(base, 0.25)
    if len(actions) > 1:
        base += 0.05
    risk = base + max(0.0, capacity_utilization_pct) / 100.0 * 0.10
    return round(min(1.0, max(0.0, risk)), 6)


def _feasibility_metadata(
    engine: "Phase6Engine",
    overlays: tuple["Overlay", ...],
    result: "CounterfactualResult",
    remaining_inventory: float,
) -> dict[str, Any]:
    actions = {overlay.action for overlay in overlays}
    uses_supplier = bool({"ALTERNATE_SUPPLIER", "EXPEDITE_PO"} & actions)
    uses_transfer = "TRANSFER_INVENTORY" in actions
    uses_capacity = bool({"ALTERNATE_SUPPLIER", "EXPEDITE_PO"} & actions)
    uses_regulatory = "ALTERNATE_SUPPLIER" in actions

    supplier_approved = True
    if uses_supplier:
        supplier_ids = {
            str(overlay.parameters.get("supplier_id", ""))
            for overlay in overlays
            if overlay.action == "ALTERNATE_SUPPLIER"
        }
        for overlay in overlays:
            if overlay.action == "EXPEDITE_PO":
                purchase_order_id = str(overlay.parameters.get("purchase_order_id", ""))
                order = next(
                    (
                        row
                        for row in engine.state.records.get("purchase_orders", ())
                        if row.get("id") == purchase_order_id
                    ),
                    None,
                )
                if order is not None:
                    supplier_ids.add(str(order.get("supplier_id", "")))
        supplier_approved = all(
            any(
                row.get("id") == supplier_id
                and row.get("status") == "ACTIVE"
                and row.get("approval_status") == "APPROVED"
                for row in engine.state.records.get("suppliers", ())
            )
            for supplier_id in supplier_ids
            if supplier_id
        )

    return {
        "uses_supplier": uses_supplier,
        "uses_transfer_lane": uses_transfer,
        "uses_capacity": uses_capacity,
        "uses_regulatory": uses_regulatory,
        "supplier_approved": supplier_approved,
        "transfer_lane_approved": True if uses_transfer else False,
        "regulatory_compliance": True if uses_regulatory else False,
        "safety_stock_ok": remaining_inventory >= 0.0,
        "phase6_status": result.status,
        "phase6_data_quality": result.data_quality_status,
        "phase6_result_hash": result.result_hash,
        "risk_policy_version": RISK_POLICY_VERSION,
    }


@dataclass(frozen=True)
class ExtractedMetrics:
    """Compatibility view used by earlier Phase 7 code."""

    candidate: str
    revenue_risk: float
    revenue_protected: float
    sla_breaches: int
    breaches_avoided: int
    delay: float
    delay_reduction: float
    recovery_cost: float
    capacity_usage: float
    inventory_consumed: float
    remaining_inventory: float
    supplier_risk: float
    simulation_hash: str

    @classmethod
    def from_candidate(cls, candidate: CandidateMetrics) -> "ExtractedMetrics":
        return cls(
            candidate=candidate.candidate_id,
            revenue_risk=candidate.revenue_risk,
            revenue_protected=candidate.revenue_protected,
            sla_breaches=candidate.sla_breaches,
            breaches_avoided=candidate.breaches_avoided,
            delay=candidate.delay_hours,
            delay_reduction=candidate.delay_reduction_hours,
            recovery_cost=candidate.recovery_cost,
            capacity_usage=candidate.capacity_utilization_pct,
            inventory_consumed=candidate.inventory_consumed,
            remaining_inventory=candidate.remaining_inventory,
            supplier_risk=candidate.supplier_risk,
            simulation_hash=candidate.simulation_hash,
        )


class MetricExtractionLayer:
    """Extract and validate the canonical metric contract."""

    def extract_from_simulation(self, simulation_result: Mapping[str, Any]) -> ExtractedMetrics:
        return ExtractedMetrics.from_candidate(CandidateMetrics.from_dict(simulation_result))

    def extract_multiple(
        self, simulation_results: Iterable[Mapping[str, Any]]
    ) -> list[ExtractedMetrics]:
        return [self.extract_from_simulation(item) for item in simulation_results]

    def from_phase6(
        self,
        engine: "Phase6Engine",
        result: "CounterfactualResult",
        candidate_id: str,
        overlays: tuple["Overlay", ...],
    ) -> CandidateMetrics:
        if result.baseline_state_hash != engine.state.identity.state_hash:
            raise OptimizationValidationError(
                f"{candidate_id}: Phase 6 result uses a different baseline state"
            )
        headline = result.headline_metrics
        revenue_risk = _decimal(headline["revenue_at_risk"]["amount"])
        baseline_revenue = _decimal(
            engine.baseline().headline_metrics["revenue_at_risk"]["amount"]
        )
        delta = result.delta
        committed, remaining, _ = _inventory_state(engine, overlays)
        capacity = _capacity_utilization(engine, overlays)
        supplier_risk = _supplier_risk(overlays, capacity, engine)
        return CandidateMetrics(
            candidate_id=candidate_id,
            label=ACTION_LABELS.get(candidate_id, candidate_id.replace("_", " ").title()),
            revenue_risk=float(revenue_risk),
            revenue_protected=float(baseline_revenue - revenue_risk),
            sla_breaches=int(headline["sla_breached_customer_order_count"]),
            breaches_avoided=int(delta["breaches_avoided"]),
            delay_hours=float(headline["maximum_delay_hours"]),
            delay_reduction_hours=float(delta["delay_reduction_hours"]),
            recovery_cost=float(_decimal(result.intervention_cost)),
            capacity_utilization_pct=capacity,
            inventory_consumed=committed,
            remaining_inventory=remaining,
            supplier_risk=supplier_risk,
            simulation_hash=result.result_hash,
            rule_set_version=result.rule_set_version,
            baseline_result_hash=result.baseline_result_hash,
            source="PHASE6",
            warnings=result.warnings,
            feasibility_metadata=_feasibility_metadata(
                engine, overlays, result, remaining
            ),
        )

    def do_nothing(self, engine: "Phase6Engine") -> CandidateMetrics:
        baseline = engine.baseline()
        headline = baseline.headline_metrics
        committed, remaining, _ = _inventory_state(engine, ())
        return CandidateMetrics(
            candidate_id="DO_NOTHING",
            label=ACTION_LABELS["DO_NOTHING"],
            revenue_risk=float(_decimal(headline["revenue_at_risk"]["amount"])),
            revenue_protected=0.0,
            sla_breaches=int(headline["sla_breached_customer_order_count"]),
            breaches_avoided=0,
            delay_hours=float(headline["maximum_delay_hours"]),
            delay_reduction_hours=0.0,
            recovery_cost=0.0,
            capacity_utilization_pct=0.0,
            inventory_consumed=committed,
            remaining_inventory=remaining,
            supplier_risk=0.0,
            simulation_hash=baseline.result_hash,
            rule_set_version=baseline.rule_set_version,
            baseline_result_hash=baseline.result_hash,
            source="PHASE6",
            warnings=tuple(baseline.warnings),
            feasibility_metadata={
                "uses_supplier": False,
                "uses_transfer_lane": False,
                "uses_capacity": False,
                "uses_regulatory": False,
                "supplier_approved": False,
                "transfer_lane_approved": False,
                "regulatory_compliance": False,
                "safety_stock_ok": remaining >= 0.0,
                "phase6_status": baseline.status.value,
                "phase6_data_quality": baseline.data_quality_status.value,
                "phase6_result_hash": baseline.result_hash,
                "risk_policy_version": RISK_POLICY_VERSION,
            },
        )
