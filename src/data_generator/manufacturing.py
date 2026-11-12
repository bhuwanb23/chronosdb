"""Phase 4G production, batch, material, and capacity generation."""

from __future__ import annotations

import csv
import math
from datetime import UTC, datetime, timedelta
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


def build_manufacturing(
    profile: ReleaseProfile,
    aliases: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    source_root = profile.root / "data" / "generated" / "operational" / profile.source_scale
    source_orders = _read_csv(source_root / "production_orders.csv")
    production_orders: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    batches: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    allocations: list[dict[str, Any]] = []
    golden_ids = ("MO-0876", "MO-0882", "MO-0889")
    golden_starts = (
        "2026-11-12T02:30:00Z",
        "2026-11-15T02:30:00Z",
        "2026-11-18T02:30:00Z",
    )
    for index, row in enumerate(source_orders, start=1):
        is_golden = index <= 3
        order_id = golden_ids[index - 1] if is_golden else f"MO-P4-{index:06d}"
        quantity = Decimal("200") if is_golden else Decimal(row["planned_quantity"])
        product_id = "PRD-CONTROLLER-X" if is_golden else _map(row["product_id"], aliases)
        facility_id = "FAC-PUNE" if is_golden else row["facility_id"]
        start = golden_starts[index - 1] if is_golden else row["planned_start"]
        completion = (
            "2026-11-14T02:30:00Z"
            if is_golden and index == 1
            else "2026-11-17T02:30:00Z"
            if is_golden and index == 2
            else "2026-11-20T02:30:00Z"
            if is_golden
            else row["planned_completion"]
        )
        status = "PLANNED" if is_golden else "RELEASED" if index % 4 == 0 else "PLANNED"
        production_orders.append(
            {
                "id": order_id,
                "production_order_id": order_id,
                "product_id": product_id,
                "facility_id": facility_id,
                "planned_quantity": str(quantity),
                "completed_quantity": "0",
                "planned_start_time": start,
                "planned_completion_time": completion,
                "actual_start_time": "",
                "actual_completion_time": "",
                "priority": "HIGH" if is_golden else row.get("priority", "MEDIUM"),
                "status": status,
                "batch_size": "100",
                "source_phase3_id": row["id"],
            }
        )
        statuses.append(
            {
                "id": f"MO-STATUS-{index:06d}-01",
                "production_order_id": order_id,
                "status": status,
                "event_time": start,
                "recorded_at": start,
            }
        )
        component_id = "CMP-MCU-42" if is_golden else "CMP-0002"
        required = quantity * Decimal("2")
        requirements.append(
            {
                "id": f"PMR-P4-{index:06d}",
                "production_order_id": order_id,
                "component_id": component_id,
                "remaining_quantity": str(quantity),
                "bom_quantity": "2",
                "scrap_factor": "0",
                "required_quantity": str(Decimal(math.ceil(required))),
                "consumption_convention": "BATCH_START",
            }
        )
        if is_golden:
            for batch_index in range(2):
                batch_start = (
                    datetime.fromisoformat(start.replace("Z", "+00:00"))
                    + timedelta(days=batch_index)
                ).isoformat().replace("+00:00", "Z")
                material_quantity = "200" if index <= 2 else "0"
                batches.append(
                    {
                        "id": f"BATCH-{order_id}-{batch_index + 1:02d}",
                        "production_order_id": order_id,
                        "facility_id": "FAC-PUNE",
                        "warehouse_id": "WH-PUNE",
                        "component_id": "CMP-MCU-42",
                        "batch_date": batch_start[:10],
                        "batch_start_time": batch_start,
                        "quantity": "100",
                        "material_quantity": material_quantity,
                        "status": "RELEASED" if material_quantity != "0" else "MATERIAL_BLOCKED",
                    }
                )
        if is_golden:
            allocations.append(
                {
                    "id": f"PMA-{order_id}",
                    "production_order_id": order_id,
                    "component_id": "CMP-MCU-42",
                    "allocated_quantity": "400" if index <= 2 else "0",
                    "allocation_status": "ALLOCATED" if index <= 2 else "BLOCKED",
                }
            )
    capacity: list[dict[str, Any]] = []
    start_date = datetime(2026, 11, 11, tzinfo=UTC)
    for day in range(profile.snapshot_days):
        current = start_date + timedelta(days=day)
        date_value = current.date().isoformat()
        for facility_id, capacity_value in (("FAC-PUNE", "100"), ("FAC-CHENNAI", "80")):
            reserved = sum(
                Decimal(batch["quantity"])
                for batch in batches
                if batch["facility_id"] == facility_id and batch["batch_date"] == date_value
            )
            capacity.append(
                {
                    "id": f"CAPCAL-{facility_id}-{date_value}",
                    "facility_id": facility_id,
                    "capacity_date": date_value,
                    "available_capacity": capacity_value,
                    "reserved_capacity": str(reserved),
                    "maintenance_capacity": "0",
                    "effective_capacity": str(Decimal(capacity_value)),
                }
            )
    output = release_root(profile) / "production"
    write_release_csv(output / "production_orders.csv", production_orders)
    write_release_csv(output / "production_order_status_history.csv", statuses)
    write_release_csv(output / "production_batches.csv", batches)
    write_release_csv(output / "production_material_requirements.csv", requirements)
    write_release_csv(output / "production_material_allocations.csv", allocations)
    write_release_csv(output / "facility_capacity_calendar.csv", capacity)
    return {
        "production_orders": production_orders,
        "statuses": statuses,
        "batches": batches,
        "requirements": requirements,
        "allocations": allocations,
        "capacity": capacity,
    }
