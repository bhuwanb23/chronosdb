from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import pytest

from chronosdb.impact.contracts.errors import DisruptionValidationError
from chronosdb.impact.contracts.requests import SimulationHorizon
from chronosdb.impact.disruption import Disruption, validate_disruption
from chronosdb.impact.inventory import InventoryEvent, detect_shortages
from chronosdb.impact.inventory.timeline import build_inventory_timelines
from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[2]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
END = AS_OF + timedelta(days=30)


def test_frozen_golden_artifact_has_release_headline() -> None:
    result = json.loads(
        (ROOT / "artifacts" / "phase-5" / "golden-impact-result.json").read_text(
            encoding="utf-8"
        )
    )

    assert result["headline_metrics"]["late_quantity"] == "400"
    assert result["headline_metrics"]["total_delay_unit_hours"] == "110400"
    assert result["headline_metrics"]["revenue_at_risk"] == {
        "amount": "1600000.00",
        "currency": "INR",
    }


def test_inventory_duplicate_event_identity_is_rejected() -> None:
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    duplicate = InventoryEvent(
        event_id="DUPLICATE-EVENT",
        event_time=AS_OF + timedelta(hours=1),
        event_type="PROJECTED_CONSUMPTION",
        warehouse_id="WH-PUNE",
        component_id="CMP-MCU-42",
        quantity=Decimal("1"),
    )

    with pytest.raises(ValueError, match="duplicate inventory event identity"):
        build_inventory_timelines(
            state,
            SimulationHorizon(AS_OF, END),
            projected_consumption=(duplicate, duplicate),
        )


def test_shortage_marks_horizon_without_fabricating_completion() -> None:
    allocation = SimpleNamespace(
        component_id="CMP-MCU-42",
        warehouse_id="WH-PUNE",
        production_order_id="MO-TEST",
        batch_id="MO-TEST-B01",
        required_time=AS_OF + timedelta(days=2),
        required_quantity=Decimal("200"),
        allocated_quantity=Decimal("0"),
        material_ready_time=None,
        source_lots=(),
        causal_parent_ids=("MO-TEST", "BOM-TEST"),
    )

    shortage = detect_shortages((allocation,), END)[0]

    assert shortage.shortage_type == "HORIZON_SHORTAGE"
    assert shortage.resolved_time is None


def test_invalid_disruption_interval_is_rejected() -> None:
    with pytest.raises(DisruptionValidationError):
        validate_disruption(
            Disruption(
                event_id="EVT-INVALID",
                event_type="SUPPLIER_OUTAGE",
                supplier_id="SUP-0104",
                start_time=AS_OF,
                end_time=AS_OF,
                recovery_lag=timedelta(hours=1),
                scope_type="ALL_SUPPLY",
            )
        )
