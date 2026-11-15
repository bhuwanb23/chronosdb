from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from chronosdb.impact.contracts.errors import ContractError
from chronosdb.impact.contracts.results import canonical_hash
from chronosdb.impact.disruption import Disruption, PurchaseOrderImpact
from chronosdb.impact.financial.delay import calculate_delay_hours
from chronosdb.impact.financial.revenue import calculate_revenue_at_risk, revenue_bounds
from chronosdb.impact.supply import project_receipts

AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)


def test_delay_is_non_negative_and_in_whole_hours() -> None:
    assert calculate_delay_hours(AS_OF + timedelta(hours=5), AS_OF) == 5
    assert calculate_delay_hours(AS_OF, AS_OF + timedelta(hours=5)) == 0
    assert calculate_delay_hours(None, AS_OF) == 0


def test_revenue_at_risk_uses_late_quantity_only() -> None:
    assert calculate_revenue_at_risk(Decimal("200"), Decimal("4000")) == Decimal("800000")
    assert calculate_revenue_at_risk(Decimal("0"), Decimal("4000")) == Decimal("0")
    assert revenue_bounds(Decimal("800000"), Decimal("200"), Decimal("4000"))
    assert not revenue_bounds(Decimal("800001"), Decimal("200"), Decimal("4000"))


def test_fully_received_purchase_order_has_no_outstanding_impact() -> None:
    from dataclasses import replace
    from pathlib import Path

    from chronosdb.impact.disruption import resolve_purchase_order_impacts
    from chronosdb.impact.state import ReleaseStateReconstructor

    order = {
        "id": "PO-TEST",
        "supplier_id": "SUP-TEST",
        "component_id": "CMP-TEST",
        "destination_warehouse_id": "WH-TEST",
        "ordered_quantity": "100",
        "received_quantity": "100",
        "expected_arrival_time": "2026-11-15T00:00:00Z",
        "status": "CONFIRMED",
    }
    disruption = Disruption(
        event_id="EVT-TEST",
        event_type="SUPPLIER_OUTAGE",
        supplier_id="SUP-TEST",
        start_time=AS_OF,
        end_time=AS_OF + timedelta(days=1),
        recovery_lag=timedelta(hours=0),
        scope_type="ALL_SUPPLY",
    )
    state = ReleaseStateReconstructor(Path(__file__).resolve().parents[3]).reconstruct(AS_OF)
    state = replace(
        state,
        records={
            **state.records,
            "purchase_orders": (order,),
            "suppliers": ({"id": "SUP-TEST"},),
        },
    )
    assert resolve_purchase_order_impacts(state, disruption) == ()


def test_projected_receipt_keeps_original_and_changed_values() -> None:
    impact = PurchaseOrderImpact(
        purchase_order_id="PO-TEST",
        supplier_id="SUP-TEST",
        component_id="CMP-TEST",
        warehouse_id="WH-TEST",
        outstanding_quantity=Decimal("25"),
        original_arrival=AS_OF + timedelta(days=2),
        disrupted_arrival=AS_OF + timedelta(days=5),
        delay_hours=72,
        rule_id="SUP-004",
        source_record_ids=("PO-TEST", "EVT-TEST"),
    )
    from chronosdb.impact.contracts.requests import SimulationHorizon

    receipt = project_receipts((impact,), SimulationHorizon(AS_OF, AS_OF + timedelta(days=30)))[0]
    assert receipt.quantity == Decimal("25")
    assert receipt.original_event_time == impact.original_arrival
    assert receipt.event_time == impact.disrupted_arrival


def test_canonical_hash_is_stable_for_ordered_arrays() -> None:
    first = canonical_hash({"items": [{"id": "A"}, {"id": "B"}]})
    second = canonical_hash({"items": [{"id": "A"}, {"id": "B"}]})
    assert first == second


def test_contract_rejects_invalid_request_horizon() -> None:
    from chronosdb.impact.contracts.requests import SimulationHorizon

    with pytest.raises(ContractError):
        SimulationHorizon(AS_OF, AS_OF)
