from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from ..inventory.timeline import InventoryTimeline
from .requirements import MaterialRequirement


class AllocationStatus(StrEnum):
    FULLY_ALLOCATED = "FULLY_ALLOCATED"
    PARTIALLY_ALLOCATED = "PARTIALLY_ALLOCATED"
    UNALLOCATED = "UNALLOCATED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


@dataclass
class SourceLot:
    source_id: str
    available_time: datetime
    quantity: Decimal
    remaining_quantity: Decimal
    source_type: str

    def take(self, quantity: Decimal) -> Decimal:
        taken = min(self.remaining_quantity, quantity)
        self.remaining_quantity -= taken
        return taken

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "available_time": self.available_time.isoformat().replace("+00:00", "Z"),
            "quantity": str(self.quantity),
            "source_type": self.source_type,
        }


@dataclass(frozen=True)
class MaterialAllocation:
    production_order_id: str
    batch_id: str
    component_id: str
    warehouse_id: str
    required_quantity: Decimal
    allocated_quantity: Decimal
    shortage_quantity: Decimal
    required_time: datetime
    material_ready_time: datetime | None
    status: AllocationStatus
    source_lots: tuple[dict[str, Any], ...]
    causal_parent_ids: tuple[str, ...]
    rule_id: str = "ALLOC-001"

    def to_dict(self) -> dict[str, Any]:
        return {
            "production_order_id": self.production_order_id,
            "batch_id": self.batch_id,
            "component_id": self.component_id,
            "warehouse_id": self.warehouse_id,
            "required_quantity": str(self.required_quantity),
            "allocated_quantity": str(self.allocated_quantity),
            "shortage_quantity": str(self.shortage_quantity),
            "required_time": self.required_time.isoformat().replace("+00:00", "Z"),
            "material_ready_time": (
                self.material_ready_time.isoformat().replace("+00:00", "Z")
                if self.material_ready_time
                else None
            ),
            "status": self.status.value,
            "source_lots": list(self.source_lots),
            "causal_parent_ids": list(self.causal_parent_ids),
            "rule_id": self.rule_id,
        }


def _build_lots(timeline: InventoryTimeline) -> list[SourceLot]:
    lots = [
        SourceLot(
            source_id=f"OPENING-{timeline.warehouse_id}-{timeline.component_id}",
            available_time=timeline.opening_time,
            quantity=timeline.opening_available,
            remaining_quantity=timeline.opening_available,
            source_type="OPENING_STATE",
        )
    ]
    for event in timeline.events:
        if event.delta > 0:
            lots.append(
                SourceLot(
                    source_id=event.event_id,
                    available_time=event.event_time,
                    quantity=event.delta,
                    remaining_quantity=event.delta,
                    source_type=event.event_type,
                )
            )
        elif event.delta < 0:
            remaining = -event.delta
            for lot in lots:
                if lot.available_time <= event.event_time and lot.remaining_quantity:
                    consumed = lot.take(remaining)
                    remaining -= consumed
                    if remaining <= 0:
                        break
    return lots


def allocate_materials(
    requirements: tuple[MaterialRequirement, ...],
    timelines: tuple[InventoryTimeline, ...],
    *,
    policy: str = "priority-due-date-v1",
    baseline_component_ids: set[str] | None = None,
) -> tuple[MaterialAllocation, ...]:
    """Allocate each requirement once, reserving future receipts deterministically."""
    if policy not in {"priority-due-date-v1", "fifo-v1"}:
        raise ValueError(f"unsupported allocation policy: {policy}")
    baseline_component_ids = baseline_component_ids or set()
    ordered_requirements = (
        tuple(
            sorted(
                requirements,
                key=lambda item: (
                    item.required_time,
                    item.production_order_id,
                    item.batch_id,
                    item.component_id,
                ),
            )
        )
        if policy == "fifo-v1"
        else requirements
    )
    lots_by_key = {
        (timeline.warehouse_id, timeline.component_id): _build_lots(timeline)
        for timeline in timelines
    }
    results: list[MaterialAllocation] = []
    for requirement in ordered_requirements:
        lots = lots_by_key.get((requirement.warehouse_id, requirement.component_id))
        if requirement.component_id in baseline_component_ids:
            results.append(
                MaterialAllocation(
                    production_order_id=requirement.production_order_id,
                    batch_id=requirement.batch_id,
                    component_id=requirement.component_id,
                    warehouse_id=requirement.warehouse_id,
                    required_quantity=requirement.required_quantity,
                    allocated_quantity=requirement.required_quantity,
                    shortage_quantity=Decimal("0"),
                    required_time=requirement.required_time,
                    material_ready_time=requirement.required_time,
                    status=AllocationStatus.FULLY_ALLOCATED,
                    source_lots=(
                        {
                            "source_id": f"BASELINE-{requirement.component_id}",
                            "available_time": requirement.required_time.isoformat().replace(
                                "+00:00", "Z"
                            ),
                            "quantity": str(requirement.required_quantity),
                            "allocated_quantity": str(requirement.required_quantity),
                            "source_type": "BASELINE_COMMITMENT",
                        },
                    ),
                    causal_parent_ids=requirement.causal_parent_ids,
                )
            )
            continue
        if lots is None:
            results.append(
                MaterialAllocation(
                    production_order_id=requirement.production_order_id,
                    batch_id=requirement.batch_id,
                    component_id=requirement.component_id,
                    warehouse_id=requirement.warehouse_id,
                    required_quantity=requirement.required_quantity,
                    allocated_quantity=Decimal("0"),
                    shortage_quantity=requirement.required_quantity,
                    required_time=requirement.required_time,
                    material_ready_time=None,
                    status=AllocationStatus.INSUFFICIENT_DATA,
                    source_lots=(),
                    causal_parent_ids=requirement.causal_parent_ids,
                )
            )
            continue
        immediate = Decimal("0")
        source_lots: list[dict[str, Any]] = []
        remaining = requirement.required_quantity
        for lot in lots:
            if lot.available_time > requirement.required_time or remaining <= 0:
                continue
            taken = lot.take(remaining)
            if taken:
                immediate += taken
                remaining -= taken
                source_lots.append({**lot.to_dict(), "allocated_quantity": str(taken)})
        material_ready_time = requirement.required_time if remaining <= 0 else None
        if remaining > 0:
            future_remaining = remaining
            for lot in lots:
                if lot.available_time <= requirement.required_time or future_remaining <= 0:
                    continue
                taken = lot.take(future_remaining)
                if taken:
                    future_remaining -= taken
                    source_lots.append(
                        {
                            **lot.to_dict(),
                            "allocated_quantity": str(taken),
                        }
                    )
                    material_ready_time = max(
                        material_ready_time or lot.available_time,
                        lot.available_time,
                    )
            if future_remaining > 0:
                material_ready_time = None
        status = (
            AllocationStatus.FULLY_ALLOCATED
            if immediate >= requirement.required_quantity
            else AllocationStatus.PARTIALLY_ALLOCATED
            if immediate > 0
            else AllocationStatus.UNALLOCATED
        )
        results.append(
            MaterialAllocation(
                production_order_id=requirement.production_order_id,
                batch_id=requirement.batch_id,
                component_id=requirement.component_id,
                warehouse_id=requirement.warehouse_id,
                required_quantity=requirement.required_quantity,
                allocated_quantity=immediate,
                shortage_quantity=max(Decimal("0"), requirement.required_quantity - immediate),
                required_time=requirement.required_time,
                material_ready_time=material_ready_time,
                status=status,
                source_lots=tuple(source_lots),
                causal_parent_ids=requirement.causal_parent_ids,
            )
        )
    return tuple(results)
