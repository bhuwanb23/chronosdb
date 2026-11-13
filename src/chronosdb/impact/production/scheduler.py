from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from ..contracts.requests import SimulationHorizon, parse_time
from ..materials.allocation import MaterialAllocation
from ..materials.requirements import MaterialRequirement
from ..state.reconstruction import OperationalState


def _iso(value: datetime | None) -> str | None:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z") if value else None


@dataclass(frozen=True)
class ProductionBatch:
    production_order_id: str
    batch_id: str
    facility_id: str
    product_id: str
    quantity: Decimal
    planned_start: datetime
    planned_completion: datetime
    projected_start: datetime | None
    projected_completion: datetime | None
    material_ready_time: datetime | None
    capacity_ready_time: datetime | None
    status: str
    blocking_components: tuple[str, ...] = ()
    blocking_receipts: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "production_order_id": self.production_order_id,
            "batch_id": self.batch_id,
            "facility_id": self.facility_id,
            "product_id": self.product_id,
            "quantity": str(self.quantity),
            "planned_start": _iso(self.planned_start),
            "planned_completion": _iso(self.planned_completion),
            "projected_start": _iso(self.projected_start),
            "projected_completion": _iso(self.projected_completion),
            "material_ready_time": _iso(self.material_ready_time),
            "capacity_ready_time": _iso(self.capacity_ready_time),
            "status": self.status,
            "blocking_components": list(self.blocking_components),
            "blocking_receipts": list(self.blocking_receipts),
        }


@dataclass(frozen=True)
class ProductionImpact:
    production_order_id: str
    planned_start: datetime
    planned_completion: datetime
    projected_start: datetime | None
    projected_completion: datetime | None
    delay_hours: int
    status: str
    blocking_components: tuple[str, ...]
    blocking_receipts: tuple[str, ...]
    batches: tuple[ProductionBatch, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "production_order_id": self.production_order_id,
            "planned_start": _iso(self.planned_start),
            "planned_completion": _iso(self.planned_completion),
            "projected_start": _iso(self.projected_start),
            "projected_completion": _iso(self.projected_completion),
            "delay_hours": self.delay_hours,
            "status": self.status,
            "blocking_components": list(self.blocking_components),
            "blocking_receipts": list(self.blocking_receipts),
            "batches": [batch.to_dict() for batch in self.batches],
        }


def _capacity_map(state: OperationalState) -> dict[tuple[str, str], Decimal]:
    return {
        (row.get("facility_id", ""), row.get("capacity_date", "")): Decimal(
            row.get(
                "available_capacity",
                str(
                    Decimal(row.get("effective_capacity", "0"))
                    - Decimal(row.get("reserved_capacity", "0"))
                    - Decimal(row.get("maintenance_capacity", "0"))
                ),
            )
        )
        for row in state.get("facility_capacity_calendar")
    }


def _facility_order(state: OperationalState) -> dict[str, dict[str, str]]:
    return {row.get("id", ""): row for row in state.get("production_orders")}


def _find_capacity_time(
    facility_id: str,
    start: datetime,
    quantity: Decimal,
    capacity: dict[tuple[str, str], Decimal],
    used: dict[tuple[str, str], Decimal],
    horizon: SimulationHorizon,
) -> datetime | None:
    candidate = start
    while candidate <= horizon.simulation_end_time:
        date_key = candidate.date().isoformat()
        effective = capacity.get((facility_id, date_key), Decimal("0"))
        if effective - used[(facility_id, date_key)] >= quantity:
            return candidate
        candidate += timedelta(days=1)
    return None


def schedule_production(
    state: OperationalState,
    requirements: tuple[MaterialRequirement, ...],
    allocations: tuple[MaterialAllocation, ...],
    horizon: SimulationHorizon,
    *,
    policy: str = "batch-capacity-v1",
) -> tuple[ProductionImpact, ...]:
    """Schedule stable batches without exceeding daily facility capacity."""
    if policy != "batch-capacity-v1":
        raise ValueError(f"unsupported scheduling policy: {policy}")
    orders = _facility_order(state)
    allocations_by_batch = defaultdict(list)
    for allocation in allocations:
        allocations_by_batch[allocation.batch_id].append(allocation)
    requirements_by_batch: dict[str, list[MaterialRequirement]] = defaultdict(list)
    for requirement in requirements:
        requirements_by_batch[requirement.batch_id].append(requirement)
    capacity = _capacity_map(state)
    used: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    by_order: dict[str, list[ProductionBatch]] = defaultdict(list)
    queue = sorted(
        (
            min(batch_requirements, key=lambda item: item.component_id)
            for batch_requirements in requirements_by_batch.values()
        ),
        key=lambda item: (
            item.order_priority,
            item.customer_priority,
            item.planned_start,
            item.production_order_id,
            item.batch_id,
        ),
    )
    facility_last_end: dict[str, datetime] = {}
    for requirement in queue:
        order = orders.get(requirement.production_order_id, {})
        processing_hours = Decimal("24")
        planned_completion = (
            parse_time(order.get("planned_completion_time", ""))
            if order.get("planned_completion_time")
            else requirement.required_time + timedelta(hours=24)
        )
        material_times = [
            allocation.material_ready_time
            for allocation in allocations_by_batch[requirement.batch_id]
            if allocation.material_ready_time is not None
        ]
        missing_material = [
            allocation
            for allocation in allocations_by_batch[requirement.batch_id]
            if allocation.material_ready_time is None
        ]
        material_ready = max(material_times, default=requirement.required_time)
        blocking_components = tuple(
            sorted({allocation.component_id for allocation in missing_material})
        )
        blocking_receipts = tuple(
            sorted(
                {
                    str(lot["source_id"])
                    for allocation in allocations_by_batch[requirement.batch_id]
                    for lot in allocation.source_lots
                    if str(lot.get("source_type", "")).startswith("PROJECTED")
                }
            )
        )
        if missing_material:
            projected_start = None
            capacity_ready = None
            projected_completion = None
            status = "NOT_COMPLETED_WITHIN_HORIZON"
        else:
            earliest = max(
                requirement.required_time,
                material_ready,
                facility_last_end.get(order.get("facility_id", ""), requirement.required_time),
            )
            capacity_ready = _find_capacity_time(
                order.get("facility_id", ""),
                earliest,
                requirement.batch_quantity,
                capacity,
                used,
                horizon,
            )
            projected_start = capacity_ready
            projected_completion = (
                capacity_ready + timedelta(hours=float(processing_hours))
                if capacity_ready is not None
                else None
            )
            status = (
                "COMPLETED_WITHIN_HORIZON"
                if projected_completion is not None
                and projected_completion <= horizon.simulation_end_time
                else "NOT_COMPLETED_WITHIN_HORIZON"
            )
            if projected_completion is None or projected_completion > horizon.simulation_end_time:
                projected_start = None
                projected_completion = None
            elif capacity_ready is not None:
                date_key = capacity_ready.date().isoformat()
                used[(order.get("facility_id", ""), date_key)] += requirement.batch_quantity
                facility_last_end[order.get("facility_id", "")] = projected_completion
        batch = ProductionBatch(
            production_order_id=requirement.production_order_id,
            batch_id=requirement.batch_id,
            facility_id=order.get("facility_id", ""),
            product_id=requirement.product_id,
            quantity=requirement.batch_quantity,
            planned_start=requirement.required_time,
            planned_completion=planned_completion,
            projected_start=projected_start,
            projected_completion=projected_completion,
            material_ready_time=material_ready,
            capacity_ready_time=capacity_ready,
            status=status,
            blocking_components=blocking_components,
            blocking_receipts=blocking_receipts,
        )
        by_order[requirement.production_order_id].append(batch)
    impacts: list[ProductionImpact] = []
    for order_id, batches in by_order.items():
        ordered = tuple(sorted(batches, key=lambda batch: batch.batch_id))
        projected_starts = [batch.projected_start for batch in ordered if batch.projected_start]
        projected_completions = [
            batch.projected_completion for batch in ordered if batch.projected_completion
        ]
        first = min(projected_starts) if projected_starts else None
        completion = max(projected_completions) if projected_completions else None
        order = orders[order_id]
        planned_start = parse_time(order["planned_start_time"])
        planned_completion = parse_time(order["planned_completion_time"])
        delay_hours = (
            max(0, int((completion - planned_completion).total_seconds() // 3600))
            if completion
            else 0
        )
        impacts.append(
            ProductionImpact(
                production_order_id=order_id,
                planned_start=planned_start,
                planned_completion=planned_completion,
                projected_start=first,
                projected_completion=completion,
                delay_hours=delay_hours,
                status=(
                    "COMPLETED_WITHIN_HORIZON"
                    if completion is not None
                    else "NOT_COMPLETED_WITHIN_HORIZON"
                ),
                blocking_components=tuple(
                    sorted({item for batch in ordered for item in batch.blocking_components})
                ),
                blocking_receipts=tuple(
                    sorted({item for batch in ordered for item in batch.blocking_receipts})
                ),
                batches=ordered,
            )
        )
    return tuple(sorted(impacts, key=lambda impact: impact.production_order_id))
