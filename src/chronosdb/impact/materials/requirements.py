from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import ROUND_CEILING, Decimal
from typing import Any

from ..contracts.requests import parse_time
from ..state.reconstruction import OperationalState
from .bom import select_bom_version


def _decimal(value: str | int | Decimal | None) -> Decimal:
    return Decimal(str(value or "0"))


@dataclass(frozen=True)
class MaterialRequirement:
    production_order_id: str
    batch_id: str
    product_id: str
    warehouse_id: str
    component_id: str
    required_quantity: Decimal
    batch_quantity: Decimal
    required_time: datetime
    bom_version_id: str
    bom_line_id: str
    customer_priority: int
    order_priority: int
    planned_start: datetime
    causal_parent_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "production_order_id": self.production_order_id,
            "batch_id": self.batch_id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "component_id": self.component_id,
            "required_quantity": str(self.required_quantity),
            "batch_quantity": str(self.batch_quantity),
            "required_time": self.required_time.isoformat().replace("+00:00", "Z"),
            "bom_version_id": self.bom_version_id,
            "bom_line_id": self.bom_line_id,
            "customer_priority": self.customer_priority,
            "order_priority": self.order_priority,
            "causal_parent_ids": list(self.causal_parent_ids),
        }


def _facility_warehouse(state: OperationalState, facility_id: str) -> str:
    links = [
        row
        for row in state.get("warehouse_facility_links")
        if row.get("facility_id") == facility_id
    ]
    if not links:
        return ""
    return sorted(links, key=lambda row: row.get("id", ""))[0].get("warehouse_id", "")


def _priority_value(value: str) -> int:
    return {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(value.upper(), 4)


def build_material_requirements(
    state: OperationalState,
    as_of: datetime,
    simulation_end: datetime | None = None,
    component_ids: set[str] | None = None,
    production_order_ids: set[str] | None = None,
) -> tuple[MaterialRequirement, ...]:
    customer_priority: dict[str, int] = {}
    line_to_order = {
        row.get("customer_order_line_id", row.get("id", "")): row.get(
            "customer_order_id", ""
        )
        for row in state.get("customer_order_lines")
    }
    order_priority = {
        row.get("customer_order_id", ""): _priority_value(row.get("priority", ""))
        for row in state.get("customer_orders")
    }
    for allocation in state.get("production_customer_allocations"):
        line_id = allocation.get("customer_order_line_id", "")
        production_order_id = allocation.get("production_order_id", "")
        priority = order_priority.get(line_to_order.get(line_id, ""), 4)
        customer_priority[production_order_id] = min(
            priority,
            customer_priority.get(production_order_id, 4),
        )
    requirements: list[MaterialRequirement] = []
    for order in state.get("production_orders"):
        if production_order_ids is not None and order.get("id") not in production_order_ids:
            continue
        if order.get("status", "").upper() in {"CANCELLED", "COMPLETED", "CLOSED"}:
            continue
        if not order.get("planned_start_time"):
            continue
        planned_start = parse_time(order["planned_start_time"])
        if planned_start < as_of or (simulation_end is not None and planned_start > simulation_end):
            continue
        planned_quantity = _decimal(order.get("planned_quantity"))
        remaining_quantity = max(
            Decimal("0"),
            planned_quantity - _decimal(order.get("completed_quantity")),
        )
        if remaining_quantity <= 0:
            continue
        batch_size = _decimal(order.get("batch_size")) or Decimal("100")
        batch_count = int(
            (remaining_quantity / batch_size).to_integral_value(rounding=ROUND_CEILING)
        )
        bom, lines = select_bom_version(state, order.get("product_id", ""), planned_start)
        warehouse_id = _facility_warehouse(state, order.get("facility_id", ""))
        for batch_index in range(batch_count):
            batch_quantity = min(
                batch_size,
                remaining_quantity - (Decimal(batch_index) * batch_size),
            )
            batch_id = f"{order['id']}-B{batch_index + 1:02d}"
            required_time = planned_start + timedelta(days=batch_index)
            for line in lines:
                if component_ids is not None and line.component_id not in component_ids:
                    continue
                gross = (
                    batch_quantity
                    * line.quantity_per
                    * (Decimal("1") + line.scrap_factor)
                )
                required = (
                    gross.to_integral_value(rounding=ROUND_CEILING)
                    if gross != gross.to_integral_value()
                    else gross
                )
                requirements.append(
                    MaterialRequirement(
                        production_order_id=order["id"],
                        batch_id=batch_id,
                        product_id=order.get("product_id", ""),
                        warehouse_id=warehouse_id,
                        component_id=line.component_id,
                        required_quantity=required,
                        batch_quantity=batch_quantity,
                        required_time=required_time,
                        bom_version_id=bom.bom_version_id,
                        bom_line_id=line.line_id,
                        customer_priority=customer_priority.get(order["id"], 4),
                        order_priority=_priority_value(order.get("priority", "")),
                        planned_start=planned_start,
                        causal_parent_ids=(order["id"], line.line_id),
                    )
                )
    return tuple(
        sorted(
            requirements,
            key=lambda item: (
                item.order_priority,
                item.customer_priority,
                item.required_time,
                item.production_order_id,
                item.batch_id,
                item.component_id,
            ),
        )
    )
