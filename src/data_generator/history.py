"""Phase 4I temporal, bitemporal, and historical replay generation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from .release_export import write_release_csv, write_release_json
from .release_profile import ReleaseProfile, release_root

REFERENCE_TIME = datetime(2026, 11, 11, 2, 30, tzinfo=UTC)
SIGNS = {
    "OPENING_BALANCE": Decimal("1"),
    "PURCHASE_RECEIPT": Decimal("1"),
    "PRODUCTION_ISSUE": Decimal("-1"),
    "TRANSFER_DISPATCH": Decimal("-1"),
    "TRANSFER_RECEIPT": Decimal("1"),
}


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_history(
    profile: ReleaseProfile,
    master: dict[str, list[dict[str, Any]]],
    procurement: dict[str, list[dict[str, Any]]],
    inventory: dict[str, list[dict[str, Any]]],
    demand: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Generate deterministic temporal fixtures and exact ledger checkpoints."""
    versions: list[dict[str, Any]] = []
    for index, agreement in enumerate(master["supplier_component_agreements"][:20], start=1):
        versions.append(
            {
                "id": f"EV-AGR-{index:04d}",
                "entity_type": "SUPPLIER_COMPONENT_AGREEMENT",
                "entity_id": agreement["id"],
                "version": "1",
                "effective_from": agreement["effective_from"],
                "effective_to": agreement["effective_to"],
                "recorded_at": agreement["effective_from"],
                "status": "ACTIVE",
            }
        )
    for index, bom in enumerate(master["bom_versions"][:10], start=1):
        versions.append(
            {
                "id": f"EV-BOM-{index:04d}",
                "entity_type": "BOM_VERSION",
                "entity_id": bom["id"],
                "version": bom["version"],
                "effective_from": bom["effective_from"],
                "effective_to": bom["effective_to"],
                "recorded_at": bom["effective_from"],
                "status": bom["status"],
            }
        )
    versions.extend(
        [
            {
                "id": "EV-SAFETY-MCU-01",
                "entity_type": "SAFETY_STOCK_POLICY",
                "entity_id": "WH-CHENNAI-CMP-MCU-42",
                "version": "1",
                "effective_from": "2026-05-15T02:30:00Z",
                "effective_to": "2026-11-09T04:35:00Z",
                "recorded_at": "2026-05-15T02:30:00Z",
                "status": "SUPERSEDED",
            },
            {
                "id": "EV-SAFETY-MCU-02",
                "entity_type": "SAFETY_STOCK_POLICY",
                "entity_id": "WH-CHENNAI-CMP-MCU-42",
                "version": "2",
                "effective_from": "2026-11-09T04:35:00Z",
                "effective_to": "2026-12-11T02:30:00Z",
                "recorded_at": "2026-11-09T04:35:00Z",
                "status": "ACTIVE",
            },
        ]
    )
    business_events = [
        {
            "id": "BE-PO-DELAY-2208",
            "event_type": "PURCHASE_ORDER_DELAY",
            "entity_type": "PURCHASE_ORDER",
            "entity_id": "PO-2208",
            "event_time": "2026-11-11T02:30:00Z",
            "reported_time": "2026-11-11T05:00:00Z",
            "ingested_time": "2026-11-11T05:05:00Z",
            "recorded_at": "2026-11-11T05:05:00Z",
        },
        {
            "id": "BE-INVENTORY-CORRECTION-001",
            "event_type": "INVENTORY_CORRECTION",
            "entity_type": "INVENTORY_BALANCE",
            "entity_id": "WH-CHENNAI-CMP-MCU-42",
            "event_time": "2026-11-08T11:30:00Z",
            "reported_time": "2026-11-09T04:30:00Z",
            "ingested_time": "2026-11-09T04:35:00Z",
            "recorded_at": "2026-11-09T04:35:00Z",
        },
        {
            "id": "BE-DISRUPTION-REPORT-001",
            "event_type": "DISRUPTION_REPORTED",
            "entity_type": "SUPPLIER",
            "entity_id": "SUP-0104",
            "event_time": "2026-11-11T02:30:00Z",
            "reported_time": "2026-11-11T03:00:00Z",
            "ingested_time": "2026-11-11T03:05:00Z",
            "recorded_at": "2026-11-11T03:05:00Z",
        },
    ]
    late_records = [
        {
            "id": "LATE-INV-CORRECTION-001",
            "source_event_id": "BE-INVENTORY-CORRECTION-001",
            "effective_time": "2026-11-08T11:30:00Z",
            "reported_time": "2026-11-09T04:30:00Z",
            "ingested_time": "2026-11-09T04:35:00Z",
            "visible_before_ingested": "false",
            "visible_after_ingested": "true",
            "completed_scenario_immutable": "true",
        }
    ]
    transactions = inventory["transactions"]
    checkpoints: list[dict[str, Any]] = []
    golden_key = ("WH-CHENNAI", "CMP-MCU-42")
    for index in range(10):
        checkpoint_time = REFERENCE_TIME + timedelta(days=index)
        quantity = Decimal("0")
        for transaction in transactions:
            if (
                transaction["warehouse_id"],
                transaction["component_id"],
            ) == golden_key and transaction["event_time"] <= _iso(checkpoint_time):
                quantity += Decimal(str(transaction["quantity"])) * SIGNS[
                    transaction["transaction_type"]
                ]
        checkpoints.append(
            {
                "id": f"HIST-CHK-{index + 1:04d}",
                "checkpoint_time": _iso(checkpoint_time),
                "warehouse_id": golden_key[0],
                "component_id": golden_key[1],
                "expected_on_hand_quantity": str(quantity),
                "reconstruction_method": "EVENT_LEDGER_REPLAY",
            }
        )
    expectations = {
        "reference_time": _iso(REFERENCE_TIME),
        "half_open_interval": "[effective_from,effective_to)",
        "checkpoint_count": len(checkpoints),
        "late_arrival_cases": [
            {
                "scenario_id": "SCN-HIST-BEFORE-INGEST",
                "freeze_time": "2026-11-09T04:34:59Z",
                "uses_correction": False,
            },
            {
                "scenario_id": "SCN-HIST-AFTER-INGEST",
                "freeze_time": "2026-11-09T04:35:00Z",
                "uses_correction": True,
            },
            {
                "scenario_id": "SCN-HIST-COMPLETED",
                "freeze_time": "2026-11-10T10:00:00Z",
                "uses_correction": False,
                "reason": "completed scenario state is immutable",
            },
        ],
        "source_counts": {
            "purchase_orders": len(procurement["purchase_orders"]),
            "customer_orders": len(demand["orders"]),
        },
    }
    output = release_root(profile) / "history"
    write_release_csv(output / "entity_versions.csv", versions)
    write_release_csv(output / "business_events.csv", business_events)
    write_release_csv(output / "late_arriving_records.csv", late_records)
    write_release_csv(output / "historical_inventory_checkpoints.csv", checkpoints)
    write_release_json(output / "replay_expectations.json", expectations)
    return {
        "entity_versions": versions,
        "business_events": business_events,
        "late_arriving_records": late_records,
        "historical_inventory_checkpoints": checkpoints,
        "replay_expectations": expectations,
    }
