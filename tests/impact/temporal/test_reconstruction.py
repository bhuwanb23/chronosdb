from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from chronosdb.impact.state import ReleaseStateReconstructor

ROOT = Path(__file__).resolve().parents[3]
AS_OF = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)


def test_state_has_no_future_operational_events() -> None:
    state = ReleaseStateReconstructor(ROOT).reconstruct(AS_OF)
    for row in state.get("purchase_order_receipts"):
        receipt_time = datetime.fromisoformat(
            row["receipt_time"].replace("Z", "+00:00")
        )
        assert receipt_time <= AS_OF
    for row in state.get("inventory_transactions"):
        event_time = datetime.fromisoformat(row["event_time"].replace("Z", "+00:00"))
        assert event_time <= AS_OF


def test_late_arriving_record_is_excluded(monkeypatch) -> None:
    reconstructor = ReleaseStateReconstructor(ROOT)
    records = reconstructor._read_records()
    records["purchase_orders"].append(
        {
            "id": "PO-LATE",
            "supplier_id": "SUP-0104",
            "component_id": "CMP-MCU-42",
            "destination_warehouse_id": "WH-PUNE",
            "ordered_quantity": "1",
            "received_quantity": "0",
            "expected_arrival_time": "2026-11-20T00:00:00Z",
            "order_time": "2026-11-11T00:00:00Z",
            "ingested_time": "2026-11-12T00:00:00Z",
            "status": "CONFIRMED",
        }
    )
    monkeypatch.setattr(reconstructor, "_read_records", lambda: records)
    state = reconstructor.reconstruct(AS_OF)
    assert not any(row["id"] == "PO-LATE" for row in state.get("purchase_orders"))


def test_latest_snapshot_only_is_retained(monkeypatch) -> None:
    reconstructor = ReleaseStateReconstructor(ROOT)
    records = reconstructor._read_records()
    records["inventory_snapshots_daily"] = [
        {
            "id": "SNAP-OLD",
            "warehouse_id": "WH-PUNE",
            "component_id": "CMP-MCU-42",
            "snapshot_time": "2026-11-10T02:30:00Z",
        },
        {
            "id": "SNAP-NEW",
            "warehouse_id": "WH-PUNE",
            "component_id": "CMP-MCU-42",
            "snapshot_time": "2026-11-11T02:30:00Z",
        },
    ]
    monkeypatch.setattr(reconstructor, "_read_records", lambda: records)
    state = reconstructor.reconstruct(AS_OF)
    assert [row["id"] for row in state.get("inventory_snapshots_daily")] == ["SNAP-NEW"]
