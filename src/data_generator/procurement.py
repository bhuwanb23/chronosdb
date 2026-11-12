"""Phase 4E procurement and inbound-supply release generation."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

from .release_export import write_release_csv
from .release_profile import ReleaseProfile, release_root


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _map(value: str, aliases: dict[str, str]) -> str:
    return aliases.get(value, value)


def build_procurement(
    profile: ReleaseProfile,
    aliases: dict[str, str],
    master: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    source_root = profile.root / "data" / "generated" / "operational" / profile.source_scale
    source = _read_csv(source_root / "purchase_orders.csv")
    purchase_orders: list[dict[str, Any]] = []
    status_history: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    capacity_by_key: dict[tuple[str, str], Decimal] = defaultdict(lambda: Decimal("0"))
    for agreement in (master or {}).get("supplier_component_agreements", []):
        key = (agreement["supplier_id"], agreement["component_id"])
        valid_days = (
            date.fromisoformat(agreement["effective_to"][:10])
            - date.fromisoformat(agreement["effective_from"][:10])
        ).days + 1
        capacity_by_key[key] += Decimal(str(agreement["daily_capacity_units"])) * valid_days
    for index, row in enumerate(source, start=1):
        golden = index == 1
        order_id = "PO-2208" if golden else f"PO-P4-{index:06d}"
        supplier_id = "SUP-0104" if golden else _map(row["supplier_id"], aliases)
        component_id = "CMP-MCU-42" if golden else _map(row["component_id"], aliases)
        ordered = Decimal("800") if golden else Decimal(row["ordered_quantity"])
        received = Decimal("0") if golden else Decimal(row["received_quantity"])
        expected = "2026-11-13T00:00:00Z" if golden else row["expected_arrival"]
        actual = "" if golden or received == 0 else expected
        status = (
            "CONFIRMED"
            if golden or not received
            else "RECEIVED"
            if received == ordered
            else "PARTIALLY_RECEIVED"
        )
        purchase_orders.append(
            {
                "id": order_id,
                "purchase_order_id": order_id,
                "supplier_id": supplier_id,
                "component_id": component_id,
                "destination_warehouse_id": (
                    "WH-PUNE"
                    if golden
                    else _map(row["destination_warehouse_id"], aliases)
                ),
                "ordered_quantity": str(ordered),
                "received_quantity": str(received),
                "outstanding_quantity": str(ordered - received),
                "order_time": row["order_time"],
                "confirmed_time": row["order_time"],
                "expected_arrival_time": expected,
                "actual_arrival_time": actual,
                "status": status,
                "unit_cost_inr": "1000.00" if golden else row["unit_price_inr"],
                "currency": "INR",
                "expedite_eligible": "false" if golden else "true",
                "effective_state_time": row["order_time"],
                "source_phase3_id": row["id"],
            }
        )
        status_history.append(
            {
                "id": f"POSTATUS-{index:06d}-01",
                "purchase_order_id": order_id,
                "status": "CONFIRMED",
                "event_time": row["order_time"],
                "recorded_at": row["order_time"],
            }
        )
        if received:
            status_history.append(
                {
                    "id": f"POSTATUS-{index:06d}-02",
                    "purchase_order_id": order_id,
                    "status": status,
                    "event_time": actual,
                    "recorded_at": actual,
                }
            )
            receipts.append(
                {
                    "id": f"RECEIPT-{index:06d}",
                    "purchase_order_id": order_id,
                    "receipt_time": actual,
                    "quantity": str(received),
                    "warehouse_id": purchase_orders[-1]["destination_warehouse_id"],
                    "component_id": component_id,
                }
            )
    capacity = [
        {
            "id": f"SUPCAP-{index:06d}",
            "supplier_id": supplier_id,
            "component_id": component_id,
            "capacity_date": "2026-11-11",
            "available_capacity": str(quantity),
            "reserved_capacity": "0",
            "effective_capacity": str(quantity),
            "currency": "INR",
        }
        for index, ((supplier_id, component_id), quantity) in enumerate(
            sorted(capacity_by_key.items()), start=1
        )
    ]
    output = release_root(profile) / "operations"
    write_release_csv(output / "purchase_orders.csv", purchase_orders)
    write_release_csv(output / "purchase_order_status_history.csv", status_history)
    write_release_csv(output / "purchase_order_receipts.csv", receipts)
    write_release_csv(output / "supplier_capacity_calendar.csv", capacity)
    return {
        "purchase_orders": purchase_orders,
        "status_history": status_history,
        "receipts": receipts,
        "capacity": capacity,
    }
