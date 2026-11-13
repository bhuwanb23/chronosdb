from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from chronosdb.impact.contracts import ImpactRequest, SimulationHorizon
from chronosdb.impact.disruption import (
    Disruption,
    resolve_purchase_order_impacts,
    validate_disruption,
)
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor
from chronosdb.impact.supply import project_receipts

ROOT = Path(__file__).resolve().parents[2]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)


def _state():
    return ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)


def _disruption(state) -> Disruption:
    return Disruption.from_state(state, "EVT-GOLD-001")


def test_request_contract_normalizes_utc_and_validates_horizon() -> None:
    request = ImpactRequest.from_dict(
        {
            "scenario_id": "SCN-GOLD-001",
            "as_of_time": "2026-11-11T02:30:00+00:00",
            "simulation_end_time": "2026-12-11T02:30:00+00:00",
            "disruption_event_id": "EVT-GOLD-001",
            "rule_set_version": "impact-rules-v1.0.0",
            "allocation_policy": "priority-due-date-v1",
            "scheduling_policy": "batch-capacity-v1",
        }
    )
    assert request.horizon.days == 30


def test_state_hash_is_stable_and_golden_purchase_order_is_reconstructed() -> None:
    first = _state()
    second = _state()
    assert first.identity.state_hash == second.identity.state_hash
    assert any(row["id"] == "PO-2208" for row in first.get("purchase_orders"))


def test_golden_supplier_outage_projects_outstanding_supply_once() -> None:
    state = _state()
    disruption = _disruption(state)
    validate_disruption(disruption)
    impacts = resolve_purchase_order_impacts(state, disruption)
    assert len(impacts) == 1
    assert impacts[0].purchase_order_id == "PO-2208"
    assert str(impacts[0].outstanding_quantity) == "800"
    assert impacts[0].delay_hours == 338
    horizon = SimulationHorizon(AS_OF, AS_OF + timedelta(days=30))
    receipts = project_receipts(impacts, horizon)
    assert [item.event_id for item in receipts] == ["RCPT-PROJ-PO-2208"]
    assert receipts[0].within_horizon is True


def test_pipeline_is_deterministic_for_same_state_and_rules() -> None:
    state = _state()
    disruption = _disruption(state)
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    horizon = SimulationHorizon(AS_OF, AS_OF + timedelta(days=30))
    first = calculate_impact(state, disruption, horizon, rules).to_dict()
    second = calculate_impact(state, disruption, horizon, rules).to_dict()
    assert first == second
    assert first["affected_purchase_orders"][0]["purchase_order_id"] == "PO-2208"
