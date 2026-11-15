"""Deterministic Phase 6 counterfactual simulation on top of the Phase 5 engine.

The engine never mutates the reconstructed operational state. Each simulation
copies the state records, adds virtual overlay records, and re-runs the Phase 5
impact engine against the same disruption, horizon, and rule set.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Mapping

from chronosdb.impact.contracts.requests import SimulationHorizon, parse_time
from chronosdb.impact.contracts.results import ImpactResult, canonical_hash
from chronosdb.impact.disruption import Disruption
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.rules.versions import RuleSet
from chronosdb.impact.state import OperationalState, ReleaseStateReconstructor

DEFAULT_SCENARIO_ID = "SCN-GOLD-001"
DEFAULT_EVENT_ID = "EVT-GOLD-001"
ACTION_ALIASES = {
    "ACTIVATE_ALT_SUPPLIER": "ALTERNATE_SUPPLIER",
    "ALTERNATE_SUPPLIER": "ALTERNATE_SUPPLIER",
    "TRANSFER_INVENTORY": "TRANSFER_INVENTORY",
    "EXPEDITE_PO": "EXPEDITE_PO",
    "RESCHEDULE_PRODUCTION": "RESCHEDULE_PRODUCTION",
}
ACTION_ORDER = {
    "TRANSFER_INVENTORY": 10,
    "ALTERNATE_SUPPLIER": 20,
    "EXPEDITE_PO": 30,
    "RESCHEDULE_PRODUCTION": 40,
}
VALID_PRIORITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}


class SimulationValidationError(ValueError):
    """Typed failure for an infeasible or malformed overlay."""


class ScenarioLedger:
    """Append-only JSONL audit ledger for simulation runs."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def record(self, result: "CounterfactualResult", runtime_ms: float) -> None:
        record = {
            "simulation_run_id": result.simulation_run_id,
            "scenario_id": result.scenario_id,
            "baseline_run_id": result.provenance["baseline_impact_run_id"],
            "baseline_result_hash": result.baseline_result_hash,
            "overlay_hash": canonical_hash(list(result.overlays)),
            "result_hash": result.result_hash,
            "runtime_ms": round(runtime_ms, 3),
            "recorded_at": _utc(datetime.now(UTC)),
            "warnings": list(result.warnings),
            "status": result.status,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def _utc(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def _records(state: OperationalState) -> dict[str, list[dict[str, str]]]:
    return {name: [dict(row) for row in rows] for name, rows in state.records.items()}


def _state_with(state: OperationalState, records: dict[str, list[dict[str, str]]]) -> OperationalState:
    return replace(
        state,
        records={name: tuple(rows) for name, rows in records.items()},
    )


def _money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


@dataclass(frozen=True)
class Overlay:
    overlay_id: str
    action: str
    parameters: Mapping[str, Any]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Overlay":
        action = str(payload.get("action", "")).upper()
        if action not in ACTION_ALIASES:
            raise SimulationValidationError(f"unsupported overlay action: {action}")
        return cls(
            overlay_id=str(payload.get("overlay_id", "")),
            action=ACTION_ALIASES[action],
            parameters=dict(payload.get("parameters", {})),
        )

    def normalized(self) -> dict[str, Any]:
        return {
            "overlay_id": self.overlay_id,
            "action": self.action,
            "parameters": dict(sorted(self.parameters.items())),
        }


@dataclass(frozen=True)
class CounterfactualResult:
    simulation_run_id: str
    scenario_id: str
    baseline_state_hash: str
    baseline_result_hash: str
    simulated_result_hash: str
    result_hash: str
    rule_set_version: str
    overlays: tuple[dict[str, Any], ...]
    events: tuple[dict[str, Any], ...]
    headline_metrics: dict[str, Any]
    delta: dict[str, Any]
    intervention_cost: str
    data_quality_status: str
    status: str
    warnings: tuple[str, ...]
    provenance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_run_id": self.simulation_run_id,
            "scenario_id": self.scenario_id,
            "baseline_state_hash": self.baseline_state_hash,
            "baseline_result_hash": self.baseline_result_hash,
            "simulated_result_hash": self.simulated_result_hash,
            "result_hash": self.result_hash,
            "rule_set_version": self.rule_set_version,
            "overlays": list(self.overlays),
            "events": list(self.events),
            "headline_metrics": self.headline_metrics,
            "delta": self.delta,
            "intervention_cost": self.intervention_cost,
            "data_quality_status": self.data_quality_status,
            "status": self.status,
            "warnings": list(self.warnings),
            "provenance": self.provenance,
        }


class Phase6Engine:
    """Run isolated intervention overlays against the frozen Phase 5 baseline."""

    def __init__(
        self,
        root: Path,
        scenario_id: str = DEFAULT_SCENARIO_ID,
        event_id: str = DEFAULT_EVENT_ID,
        horizon_days: int = 30,
    ) -> None:
        self.root = root
        scenario_path = root / "data" / "releases" / "v1.0.0" / "golden" / "scenario.json"
        self.scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        self.scenario_id = scenario_id
        self.as_of = parse_time(self.scenario["as_of_time"])
        self.horizon = SimulationHorizon(self.as_of, self.as_of + timedelta(days=horizon_days))
        self.state = ReleaseStateReconstructor(root).reconstruct(self.as_of)
        self.disruption = Disruption.from_state(self.state, event_id)
        self.rules: RuleSet = load_rule_set(
            root / "config" / "rules" / "impact-rules-v1.0.0.yaml"
        )
        self._baseline: ImpactResult | None = None

    def baseline(self) -> ImpactResult:
        if self._baseline is None:
            self._baseline = calculate_impact(
                self.state,
                self.disruption,
                self.horizon,
                self.rules,
                scenario_id=self.scenario_id,
            )
        return self._baseline

    def _opening(
        self, records: dict[str, list[dict[str, str]]], warehouse_id: str, component_id: str
    ) -> dict[str, str] | None:
        return next(
            (
                row
                for row in records["inventory_opening_balances"]
                if row.get("warehouse_id") == warehouse_id
                and row.get("component_id") == component_id
            ),
            None,
        )

    def _apply_transfer(
        self,
        records: dict[str, list[dict[str, str]]],
        overlay: Overlay,
        events: list[dict[str, Any]],
    ) -> Decimal:
        params = overlay.parameters
        component_id = str(params.get("component_id", ""))
        source = str(params.get("from_warehouse") or params.get("source_warehouse") or "")
        destination = str(
            params.get("to_warehouse") or params.get("destination_warehouse") or ""
        )
        try:
            quantity = _decimal(params.get("quantity", "0"))
        except Exception as exc:
            raise SimulationValidationError("transfer quantity must be numeric") from exc
        if not component_id or not source or not destination:
            raise SimulationValidationError("transfer requires component and warehouses")
        if quantity <= 0:
            raise SimulationValidationError("transfer quantity must be positive")
        source_opening = self._opening(records, source, component_id)
        destination_opening = self._opening(records, destination, component_id)
        if source_opening is None or destination_opening is None:
            raise SimulationValidationError("transfer warehouse/component has no opening inventory")
        available = (
            _decimal(source_opening.get("on_hand_quantity", "0"))
            - _decimal(source_opening.get("quarantined_quantity", "0"))
            - _decimal(source_opening.get("reserved_quantity", "0"))
        )
        if quantity > available:
            raise SimulationValidationError("transfer exceeds available source stock")
        safety_stock = _decimal(source_opening.get("safety_stock_quantity", "0"))
        if available - quantity < safety_stock:
            raise SimulationValidationError("transfer violates source safety stock")
        lane = next(
            (
                row
                for row in records["transfer_lanes"]
                if row.get("source_warehouse") == source
                and row.get("destination_warehouse") == destination
                and parse_time(row["active_from"]) <= self.as_of < parse_time(row["active_to"])
            ),
            None,
        )
        if lane is None:
            raise SimulationValidationError("no active transfer lane for warehouses")
        arrival = self.as_of + timedelta(hours=int(lane["lead_time_hours"]))
        if arrival > self.horizon.simulation_end_time:
            raise SimulationValidationError("transfer arrival falls outside the horizon")
        records["inventory_transactions"].extend(
            (
                {
                    "id": f"{overlay.overlay_id}-OUT",
                    "transaction_type": "EXISTING_TRANSFER_OUT",
                    "event_time": _utc(self.as_of),
                    "warehouse_id": source,
                    "component_id": component_id,
                    "quantity": str(quantity),
                    "reference_id": overlay.overlay_id,
                },
                {
                    "id": f"{overlay.overlay_id}-IN",
                    "transaction_type": "EXISTING_TRANSFER_IN",
                    "event_time": _utc(arrival),
                    "warehouse_id": destination,
                    "component_id": component_id,
                    "quantity": str(quantity),
                    "reference_id": overlay.overlay_id,
                },
            )
        )
        events.append(
            {
                "event_type": "SIM_TRANSFER_RECEIPT",
                "overlay_id": overlay.overlay_id,
                "component_id": component_id,
                "quantity": str(quantity),
                "from_warehouse": source,
                "to_warehouse": destination,
                "arrival_time": _utc(arrival),
                "lane_id": lane.get("id", ""),
            }
        )
        return _decimal(lane.get("fixed_cost", "0")) + quantity * _decimal(
            lane.get("variable_cost_per_unit", "0")
        )

    def _apply_expedition(
        self,
        records: dict[str, list[dict[str, str]]],
        overlay: Overlay,
        events: list[dict[str, Any]],
    ) -> Decimal:
        params = overlay.parameters
        purchase_order_id = str(params.get("purchase_order_id", ""))
        try:
            reduction_days = int(params.get("lead_time_reduction_days", 0))
        except Exception as exc:
            raise SimulationValidationError("expedition reduction must be an integer") from exc
        if reduction_days <= 0:
            raise SimulationValidationError("expedition reduction must be positive")
        order = next(
            (row for row in records["purchase_orders"] if row.get("id") == purchase_order_id),
            None,
        )
        if order is None:
            raise SimulationValidationError(f"unknown purchase order: {purchase_order_id}")
        if order.get("status", "").upper() in {"RECEIVED", "CANCELLED", "CLOSED"}:
            raise SimulationValidationError("purchase order cannot be expedited")
        outstanding = max(
            Decimal("0"),
            _decimal(order.get("ordered_quantity", "0"))
            - _decimal(order.get("received_quantity", "0")),
        )
        if outstanding <= 0:
            raise SimulationValidationError("purchase order has no outstanding quantity")
        disrupted_arrival = max(
            parse_time(order["expected_arrival_time"]),
            self.disruption.end_time + self.disruption.recovery_lag,
        )
        early_arrival = disrupted_arrival - timedelta(days=reduction_days)
        if early_arrival < self.as_of or early_arrival > self.horizon.simulation_end_time:
            raise SimulationValidationError("expedited arrival falls outside the horizon")
        order_time = order.get("order_time") or order.get("confirmed_time")
        if order_time and early_arrival < parse_time(order_time):
            raise SimulationValidationError("expedition precedes shipment release")
        component = order.get("component_id", "")
        warehouse = order.get("destination_warehouse_id", "")
        agreement = next(
            (
                row
                for row in records["supplier_component_agreements"]
                if row.get("supplier_id") == order.get("supplier_id")
                and row.get("component_id") == component
                and row.get("approval_status") == "APPROVED"
                and parse_time(row["effective_from"]) <= self.as_of < parse_time(row["effective_to"])
            ),
            None,
        )
        if agreement is None:
            raise SimulationValidationError("supplier has no active agreement for expedition")
        daily_capacity = _decimal(agreement.get("daily_capacity_units", "0"))
        order_time = order.get("order_time") or order.get("confirmed_time")
        production_days = max(
            1,
            (parse_time(order["expected_arrival_time"]) - parse_time(order_time)).days
            if order_time
            else reduction_days,
        )
        if daily_capacity * production_days < outstanding:
            raise SimulationValidationError("expedition exceeds supplier capability")
        order["status"] = "RECEIVED"
        order["received_quantity"] = order.get("ordered_quantity", "0")
        records["inventory_transactions"].append(
            {
                "id": f"{overlay.overlay_id}-RECEIPT",
                "transaction_type": "PURCHASE_RECEIPT",
                "event_time": _utc(early_arrival),
                "warehouse_id": warehouse,
                "component_id": component,
                "quantity": str(outstanding),
                "reference_id": purchase_order_id,
            }
        )
        events.append(
            {
                "event_type": "SIM_EXPEDITION_RECEIPT",
                "overlay_id": overlay.overlay_id,
                "purchase_order_id": purchase_order_id,
                "component_id": component,
                "quantity": str(outstanding),
                "arrival_time": _utc(early_arrival),
                "original_disrupted_arrival": _utc(disrupted_arrival),
                "reduction_days": reduction_days,
            }
        )
        return Decimal("1200") + Decimal("450") * reduction_days + Decimal("200")

    def _apply_alternate_supplier(
        self,
        records: dict[str, list[dict[str, str]]],
        overlay: Overlay,
        events: list[dict[str, Any]],
    ) -> Decimal:
        params = overlay.parameters
        supplier_id = str(params.get("supplier_id", ""))
        component_id = str(params.get("component_id", ""))
        warehouse = str(params.get("to_warehouse") or "WH-PUNE")
        supplier = next(
            (row for row in records["suppliers"] if row.get("id") == supplier_id), None
        )
        if supplier is None:
            raise SimulationValidationError(f"unknown supplier: {supplier_id}")
        if supplier.get("status") != "ACTIVE" or supplier.get("approval_status") != "APPROVED":
            raise SimulationValidationError("alternate supplier is not active and approved")
        agreement = next(
            (
                row
                for row in records["supplier_component_agreements"]
                if row.get("supplier_id") == supplier_id
                and row.get("component_id") == component_id
                and row.get("approval_status") == "APPROVED"
                and parse_time(row["effective_from"]) <= self.as_of < parse_time(row["effective_to"])
            ),
            None,
        )
        if agreement is None:
            raise SimulationValidationError("alternate supplier has no active agreement")
        quantity = _decimal(params.get("available_quantity", params.get("quantity", "0")))
        if quantity <= 0:
            raise SimulationValidationError("alternate supply quantity must be positive")
        lead_time_days = int(params.get("lead_time_days", agreement.get("lead_time_days", "0")))
        if lead_time_days <= 0:
            raise SimulationValidationError("alternate supplier lead time must be positive")
        if _decimal(agreement.get("daily_capacity_units", "0")) * lead_time_days < quantity:
            raise SimulationValidationError("alternate supplier capacity is insufficient")
        arrival = self.as_of + timedelta(days=lead_time_days)
        if arrival > self.horizon.simulation_end_time:
            raise SimulationValidationError("alternate supply falls outside the horizon")
        records["inventory_transactions"].append(
            {
                "id": f"{overlay.overlay_id}-RECEIPT",
                "transaction_type": "PURCHASE_RECEIPT",
                "event_time": _utc(arrival),
                "warehouse_id": warehouse,
                "component_id": component_id,
                "quantity": str(quantity),
                "reference_id": supplier_id,
            }
        )
        events.append(
            {
                "event_type": "SIM_ALT_SUPPLIER_RECEIPT",
                "overlay_id": overlay.overlay_id,
                "supplier_id": supplier_id,
                "component_id": component_id,
                "quantity": str(quantity),
                "arrival_time": _utc(arrival),
                "agreement_id": agreement.get("id", ""),
            }
        )
        return _decimal(agreement.get("unit_price_inr", "0")) * quantity

    def _apply_reschedule(
        self,
        records: dict[str, list[dict[str, str]]],
        overlay: Overlay,
        events: list[dict[str, Any]],
    ) -> Decimal:
        params = overlay.parameters
        production_order_id = str(
            params.get("production_order_id")
            or params.get("manufacturing_order_id")
            or ""
        )
        priority = str(params.get("priority", "")).upper()
        if priority.isdigit():
            priority = {"1": "CRITICAL", "2": "HIGH", "3": "MEDIUM", "4": "LOW"}.get(
                priority, priority
            )
        if priority not in VALID_PRIORITIES:
            raise SimulationValidationError("invalid production priority")
        order = next(
            (row for row in records["production_orders"] if row.get("id") == production_order_id),
            None,
        )
        if order is None:
            raise SimulationValidationError(f"unknown production order: {production_order_id}")
        previous = order.get("priority", "")
        order["priority"] = priority
        events.append(
            {
                "event_type": "SIM_PRODUCTION_RESCHEDULE",
                "overlay_id": overlay.overlay_id,
                "production_order_id": production_order_id,
                "previous_priority": previous,
                "priority": priority,
            }
        )
        return Decimal("12000")

    def _validate_overlay_set(self, overlays: Iterable[Overlay]) -> tuple[Overlay, ...]:
        items = tuple(overlays)
        if not items:
            raise SimulationValidationError("at least one overlay is required")
        ids = [overlay.overlay_id for overlay in items]
        if any(not overlay_id for overlay_id in ids):
            raise SimulationValidationError("every overlay requires an overlay_id")
        if len(ids) != len(set(ids)):
            raise SimulationValidationError("duplicate overlay_id")
        for overlay in items:
            if overlay.action not in ACTION_ORDER:
                raise SimulationValidationError(
                    f"unsupported overlay action: {overlay.action}"
                )
        targets = [
            (
                overlay.action,
                overlay.parameters.get("component_id")
                or overlay.parameters.get("purchase_order_id")
                or overlay.parameters.get("production_order_id"),
            )
            for overlay in items
        ]
        if len(targets) != len(set(targets)):
            raise SimulationValidationError("conflicting overlays target the same record")
        return tuple(sorted(items, key=lambda item: (ACTION_ORDER[item.action], item.overlay_id)))

    def _apply_overlays(
        self, overlays: Iterable[Overlay]
    ) -> tuple[OperationalState, tuple[dict[str, Any], ...], Decimal]:
        ordered = self._validate_overlay_set(overlays)
        records = _records(self.state)
        events: list[dict[str, Any]] = []
        total_cost = Decimal("0")
        handlers = {
            "TRANSFER_INVENTORY": self._apply_transfer,
            "EXPEDITE_PO": self._apply_expedition,
            "ALTERNATE_SUPPLIER": self._apply_alternate_supplier,
            "RESCHEDULE_PRODUCTION": self._apply_reschedule,
        }
        for overlay in ordered:
            total_cost += handlers[overlay.action](records, overlay, events)
        return _state_with(self.state, records), tuple(events), total_cost

    def _delta(self, scenario: ImpactResult, intervention_cost: Decimal) -> dict[str, Any]:
        baseline = self.baseline().headline_metrics
        current = scenario.headline_metrics
        baseline_revenue = _decimal(baseline["revenue_at_risk"]["amount"])
        scenario_revenue = _decimal(current["revenue_at_risk"]["amount"])
        baseline_breaches = int(baseline["sla_breached_customer_order_count"])
        scenario_breaches = int(current["sla_breached_customer_order_count"])
        baseline_delay = int(baseline["maximum_delay_hours"])
        scenario_delay = int(current["maximum_delay_hours"])
        revenue_protected = baseline_revenue - scenario_revenue
        return {
            "baseline_revenue_risk": _money(baseline_revenue),
            "scenario_revenue_risk": _money(scenario_revenue),
            "revenue_protected": _money(revenue_protected),
            "baseline_breaches": baseline_breaches,
            "scenario_breaches": scenario_breaches,
            "breaches_avoided": baseline_breaches - scenario_breaches,
            "baseline_delay_hours": baseline_delay,
            "scenario_delay_hours": scenario_delay,
            "delay_reduction_hours": baseline_delay - scenario_delay,
            "intervention_cost": _money(intervention_cost),
            "net_benefit": _money(revenue_protected - intervention_cost),
        }

    def run(
        self,
        overlays: Iterable[Overlay],
        ledger: ScenarioLedger | None = None,
    ) -> CounterfactualResult:
        started = time.perf_counter()
        ordered = self._validate_overlay_set(overlays)
        simulated_state, events, cost = self._apply_overlays(ordered)
        simulated = calculate_impact(
            simulated_state,
            self.disruption,
            self.horizon,
            self.rules,
            scenario_id=self.scenario_id,
        )
        baseline = self.baseline()
        delta = self._delta(simulated, cost)
        payload = {
            "scenario_id": self.scenario_id,
            "baseline_state_hash": self.state.identity.state_hash,
            "baseline_result_hash": baseline.result_hash,
            "overlays": [overlay.normalized() for overlay in ordered],
            "events": list(events),
            "simulated_result_hash": simulated.result_hash,
            "delta": delta,
            "data_quality_status": simulated.data_quality_status.value,
        }
        result_hash = canonical_hash(payload)
        result = CounterfactualResult(
            simulation_run_id=f"SIM-{result_hash[:16]}",
            scenario_id=self.scenario_id,
            baseline_state_hash=self.state.identity.state_hash,
            baseline_result_hash=baseline.result_hash,
            simulated_result_hash=simulated.result_hash,
            result_hash=result_hash,
            rule_set_version=self.rules.version,
            overlays=tuple(overlay.normalized() for overlay in ordered),
            events=events,
            headline_metrics=simulated.headline_metrics,
            delta=delta,
            intervention_cost=_money(cost),
            data_quality_status=simulated.data_quality_status.value,
            status=simulated.status.value,
            warnings=tuple(simulated.warnings),
            provenance={
                "baseline_impact_run_id": baseline.impact_run_id,
                "simulated_impact_run_id": simulated.impact_run_id,
                "state_hash": self.state.identity.state_hash,
                "disruption_event_id": self.disruption.event_id,
                "rule_set_version": self.rules.version,
                "overlay_hashes": [canonical_hash(overlay.normalized()) for overlay in ordered],
                "event_ids": [event["overlay_id"] for event in events],
            },
        )
        if ledger is not None:
            ledger.record(result, (time.perf_counter() - started) * 1000)
        return result


def load_golden_overlays(path: Path) -> dict[str, tuple[Overlay, ...]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        name: tuple(Overlay.from_dict(item) for item in items)
        for name, items in payload.items()
    }
