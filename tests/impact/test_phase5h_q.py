from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from chronosdb.impact.contracts.requests import SimulationHorizon
from chronosdb.impact.contracts.results import canonical_hash
from chronosdb.impact.disruption import Disruption
from chronosdb.impact.inventory.events import InventoryEvent
from chronosdb.impact.inventory.timeline import build_inventory_timelines
from chronosdb.impact.orchestration import calculate_impact
from chronosdb.impact.persistence import ExecutionLedger, PersistenceError
from chronosdb.impact.rules import load_rule_set
from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[2]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
END = datetime(2026, 12, 11, 2, 30, tzinfo=UTC)


def _golden_result(**kwargs):
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    disruption = Disruption.from_state(state, "EVT-GOLD-001")
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    return calculate_impact(
        state,
        disruption,
        SimulationHorizon(AS_OF, END),
        rules,
        scenario_id="SCN-GOLD-001",
        **kwargs,
    )


def test_golden_headline_matches_frozen_do_nothing_values() -> None:
    metrics = _golden_result().to_dict()["headline_metrics"]

    assert metrics["sla_breached_customer_order_count"] == 2
    assert metrics["late_quantity"] == "400"
    assert metrics["total_delay_unit_hours"] == "110400"
    assert metrics["revenue_at_risk"] == {"amount": "1600000.00", "currency": "INR"}


def test_inventory_timeline_conserves_balance() -> None:
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    event = InventoryEvent(
        event_id="TEST-RECEIPT",
        event_time=AS_OF + timedelta(days=1),
        event_type="PURCHASE_RECEIPT",
        warehouse_id="WH-PUNE",
        component_id="CMP-MCU-42",
        quantity=Decimal("10"),
    )
    timeline = next(
        item
        for item in build_inventory_timelines(
            state,
            SimulationHorizon(AS_OF, END),
            projected_consumption=(event,),
        )
        if item.warehouse_id == "WH-PUNE" and item.component_id == "CMP-MCU-42"
    )

    assert timeline.ending_balance == timeline.opening_physical + event.delta


def test_result_fingerprint_includes_execution_policies() -> None:
    first = _golden_result(allocation_policy="priority-due-date-v1").to_dict()
    second = _golden_result(allocation_policy="fifo-v1").to_dict()

    assert first["impact_run_id"] != second["impact_run_id"]


def test_execution_ledger_keeps_completed_result_immutable() -> None:
    ledger = ExecutionLedger()
    run = ledger.begin(
        impact_run_id="IR-TEST",
        scenario_id="SCN-TEST",
        request_fingerprint="a" * 64,
        input_state_hash="b" * 64,
        rule_set_version="impact-rules-v1.0.0",
    )
    ledger.complete(
        run.impact_run_id,
        status="COMPLETED",
        data_quality_status="COMPLETE",
        result_hash="c" * 64,
        payload={"result_hash": "c" * 64},
    )

    try:
        ledger.complete(
            run.impact_run_id,
            status="COMPLETED",
            data_quality_status="COMPLETE",
            result_hash="d" * 64,
            payload={"result_hash": "d" * 64},
        )
    except PersistenceError:
        pass
    else:
        raise AssertionError("completed result was mutable")


def test_canonical_hash_is_order_independent_for_mappings() -> None:
    assert canonical_hash({"a": 1, "b": 2}) == canonical_hash({"b": 2, "a": 1})
