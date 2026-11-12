"""Phase 4H customer demand, allocation, and SLA release generation."""

from __future__ import annotations

import csv
from datetime import datetime
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


def _hours_late(promised: str, projected: str) -> int:
    promised_time = datetime.fromisoformat(promised.replace("Z", "+00:00"))
    projected_time = datetime.fromisoformat(projected.replace("Z", "+00:00"))
    return max(0, int((projected_time - promised_time).total_seconds() // 3600))


def build_demand(
    profile: ReleaseProfile,
    aliases: dict[str, str],
    master: dict[str, list[dict[str, Any]]],
    manufacturing: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Create traceable demand while preserving the frozen golden narrative."""
    source_root = profile.root / "data" / "generated" / "operational" / profile.source_scale
    source_orders = _read_csv(source_root / "customer_orders.csv")
    source_lines = _read_csv(source_root / "customer_order_lines.csv")
    customers = {row["id"] for row in master["customers"]}
    production_orders = manufacturing["production_orders"]
    golden = (
        ("CO-0701", "2026-11-01T02:30:00Z", "2026-11-15T00:00:00Z", "HIGH"),
        ("CO-0704", "2026-11-02T02:30:00Z", "2026-11-18T00:00:00Z", "HIGH"),
        ("CO-0711", "2026-11-03T02:30:00Z", "2026-11-21T00:00:00Z", "HIGH"),
    )
    orders: list[dict[str, Any]] = []
    lines: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    allocations: list[dict[str, Any]] = []
    sla_assignments: list[dict[str, Any]] = []
    for index, source_order in enumerate(source_orders):
        is_golden = index < 3
        order_id = golden[index][0] if is_golden else source_order["id"]
        customer_id = source_order["customer_id"]
        if customer_id not in customers:
            customer_id = next(iter(sorted(customers)))
        order_time = golden[index][1] if is_golden else source_order["order_time"]
        priority = golden[index][3] if is_golden else source_order["priority"]
        line_source = source_lines[index % len(source_lines)]
        line_id = f"COL-{order_id}-01"
        product_id = (
            "PRD-CONTROLLER-X"
            if is_golden
            else _map(line_source["product_id"], aliases)
        )
        promised = golden[index][2] if is_golden else line_source["promised_delivery"]
        quantity = Decimal("200") if is_golden else Decimal(line_source["ordered_quantity"])
        unit_revenue = Decimal("4000") if is_golden else Decimal(line_source["unit_revenue_inr"])
        production_id = (
            ("MO-0876", "MO-0882", "MO-0889")[index]
            if is_golden
            else production_orders[index % len(production_orders)]["id"]
        )
        orders.append(
            {
                "customer_order_id": order_id,
                "customer_id": customer_id,
                "order_time": order_time,
                "promised_delivery_time": promised,
                "priority": priority,
                "sla_class": "GOLD" if is_golden else "STANDARD",
                "status": "OPEN",
                "currency": "INR",
            }
        )
        lines.append(
            {
                "customer_order_line_id": line_id,
                "customer_order_id": order_id,
                "product_id": product_id,
                "ordered_quantity": str(quantity),
                "fulfilled_quantity": "0",
                "unit_revenue": str(unit_revenue),
                "line_revenue": str(quantity * unit_revenue),
                "assigned_production_order_id": production_id,
            }
        )
        statuses.append(
            {
                "id": f"COSTATUS-{index + 1:06d}-01",
                "customer_order_id": order_id,
                "status": "OPEN",
                "event_time": order_time,
                "recorded_at": order_time,
            }
        )
        allocations.append(
            {
                "id": f"PCA-P4-{index + 1:06d}",
                "production_order_id": production_id,
                "customer_order_line_id": line_id,
                "allocated_quantity": str(quantity),
                "allocation_rank": str(index + 1),
            }
        )
        projected = promised
        late_quantity = Decimal("0")
        sla_status = "ON_TIME"
        if is_golden and index in (1, 2):
            projected = "2026-11-30T00:00:00Z" if index == 1 else "2026-12-02T00:00:00Z"
            late_quantity = quantity
            sla_status = "LATE"
        delay_hours = _hours_late(promised, projected)
        sla_assignments.append(
            {
                "id": f"SLA-P4-{index + 1:06d}",
                "customer_order_line_id": line_id,
                "sla_class": "GOLD" if is_golden else "STANDARD",
                "promised_delivery_time": promised,
                "projected_delivery_time": projected,
                "projected_on_time_quantity": str(quantity - late_quantity),
                "projected_late_quantity": str(late_quantity),
                "delay_hours": str(delay_hours),
                "sla_status": sla_status,
                "revenue_at_risk": str(late_quantity * unit_revenue),
            }
        )
    output = release_root(profile) / "demand"
    write_release_csv(output / "customer_orders.csv", orders)
    write_release_csv(output / "customer_order_lines.csv", lines)
    write_release_csv(output / "customer_order_status_history.csv", statuses)
    write_release_csv(output / "production_customer_allocations.csv", allocations)
    write_release_csv(output / "customer_sla_assignments.csv", sla_assignments)
    return {
        "orders": orders,
        "lines": lines,
        "statuses": statuses,
        "allocations": allocations,
        "sla_assignments": sla_assignments,
    }
