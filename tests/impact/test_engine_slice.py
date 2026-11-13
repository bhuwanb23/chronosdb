from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from chronosdb.impact.contracts import ImpactRequest, SimulationHorizon
from chronosdb.impact.disruption import (
    Disruption,
    PurchaseOrderImpact,
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


def test_run_identity_includes_scenario_and_horizon_inputs() -> None:
    state = _state()
    disruption = _disruption(state)
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")
    horizon = SimulationHorizon(AS_OF, AS_OF + timedelta(days=30))

    first = calculate_impact(
        state, disruption, horizon, rules, scenario_id="SCN-A"
    ).to_dict()
    second = calculate_impact(
        state,
        disruption,
        SimulationHorizon(AS_OF, AS_OF + timedelta(days=31)),
        rules,
        scenario_id="SCN-B",
    ).to_dict()

    assert first["impact_run_id"] != second["impact_run_id"]


def test_reconstruction_keeps_only_latest_snapshot_per_location(
    monkeypatch,
) -> None:
    reconstructor = ReleaseStateReconstructor(ROOT)
    records = reconstructor._read_records()
    records["inventory_snapshots_daily"] = [
        {
            "id": "SNAP-OLD",
            "warehouse_id": "WH-CHENNAI",
            "component_id": "CMP-MCU-42",
            "snapshot_time": "2026-11-10T02:30:00Z",
        },
        {
            "id": "SNAP-NEW",
            "warehouse_id": "WH-CHENNAI",
            "component_id": "CMP-MCU-42",
            "snapshot_time": "2026-11-11T02:30:00Z",
        },
    ]
    monkeypatch.setattr(reconstructor, "_read_records", lambda: records)

    state = reconstructor.reconstruct(AS_OF)

    assert [row["id"] for row in state.get("inventory_snapshots_daily")] == [
        "SNAP-NEW"
    ]


def test_filtered_empty_required_record_set_is_marked_incomplete(
    monkeypatch,
) -> None:
    reconstructor = ReleaseStateReconstructor(ROOT)
    records = reconstructor._read_records()
    records["purchase_orders"] = []
    monkeypatch.setattr(reconstructor, "_read_records", lambda: records)

    state = reconstructor.reconstruct(AS_OF)

    assert "empty record set: purchase_orders" in state.warnings


def test_receipt_before_horizon_is_out_of_horizon() -> None:
    impact = PurchaseOrderImpact(
        purchase_order_id="PO-OLD",
        supplier_id="SUP-OLD",
        component_id="CMP-OLD",
        warehouse_id="WH-OLD",
        outstanding_quantity=Decimal("5"),
        original_arrival=datetime(2026, 11, 1, tzinfo=UTC),
        disrupted_arrival=datetime(2026, 11, 5, tzinfo=UTC),
        delay_hours=96,
        rule_id="SUP-004",
        source_record_ids=("PO-OLD", "EVT-OLD"),
    )

    receipt = project_receipts(
        (impact,), SimulationHorizon(AS_OF, AS_OF + timedelta(days=30))
    )[0]

    assert receipt.within_horizon is False


def test_provenance_retains_disruption_source_without_affected_orders() -> None:
    state = _state()
    disruption = Disruption(
        event_id="EVT-NO-MATCH",
        event_type="SUPPLIER_OUTAGE",
        supplier_id="SUP-NO-MATCH",
        start_time=AS_OF,
        end_time=AS_OF + timedelta(hours=1),
        recovery_lag=timedelta(hours=1),
        scope_type="ALL_SUPPLY",
    )
    rules = load_rule_set(ROOT / "config" / "rules" / "impact-rules-v1.0.0.yaml")

    result = calculate_impact(
        state,
        disruption,
        SimulationHorizon(AS_OF, AS_OF + timedelta(days=30)),
        rules,
    ).to_dict()

    assert result["affected_purchase_orders"] == []
    assert result["provenance"]["source_record_ids"] == ["EVT-NO-MATCH"]
    assert "STATE-002" in result["provenance"]["rule_ids"]
    assert "DQ-001" in result["provenance"]["rule_ids"]
