from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from typing import Any

from ..contracts.requests import SimulationHorizon, parse_time
from ..production.scheduler import ProductionImpact
from ..state.reconstruction import OperationalState


def _iso(value: datetime | None) -> str | None:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z") if value else None


def _delivery_time(completion: datetime, lead_days: int = 1) -> datetime:
    return datetime.combine(
        completion.date() + timedelta(days=lead_days),
        time.min,
        tzinfo=UTC,
    )


@dataclass(frozen=True)
class FulfilmentSegment:
    order_line_id: str
    quantity: Decimal
    availability_time: datetime
    projected_delivery: datetime
    production_batch_id: str
    facility_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_line_id": self.order_line_id,
            "quantity": str(self.quantity),
            "availability_time": _iso(self.availability_time),
            "projected_delivery": _iso(self.projected_delivery),
            "production_batch_id": self.production_batch_id,
            "facility_id": self.facility_id,
        }


@dataclass(frozen=True)
class CustomerImpact:
    customer_order_id: str
    customer_order_line_id: str
    production_order_id: str
    product_id: str
    open_quantity: Decimal
    promised_delivery: datetime | None
    unit_revenue: Decimal | None
    segments: tuple[FulfilmentSegment, ...]
    data_quality_status: str = "COMPLETE"

    @property
    def fulfilled_quantity(self) -> Decimal:
        return sum((segment.quantity for segment in self.segments), Decimal("0"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_order_id": self.customer_order_id,
            "customer_order_line_id": self.customer_order_line_id,
            "production_order_id": self.production_order_id,
            "product_id": self.product_id,
            "open_quantity": str(self.open_quantity),
            "promised_delivery": _iso(self.promised_delivery),
            "unit_revenue": str(self.unit_revenue) if self.unit_revenue is not None else None,
            "segments": [segment.to_dict() for segment in self.segments],
            "fulfilled_quantity": str(self.fulfilled_quantity),
            "data_quality_status": self.data_quality_status,
        }


def build_customer_fulfilment(
    state: OperationalState,
    production_impacts: tuple[ProductionImpact, ...],
    horizon: SimulationHorizon,
    production_order_ids: set[str] | None = None,
    customer_order_line_ids: set[str] | None = None,
) -> tuple[CustomerImpact, ...]:
    orders = {
        row.get("customer_order_id", row.get("id", "")): row
        for row in state.get("customer_orders")
    }
    allocations = {
        row.get("customer_order_line_id", ""): row
        for row in state.get("production_customer_allocations")
    }
    production_by_id = {impact.production_order_id: impact for impact in production_impacts}
    result: list[CustomerImpact] = []
    for line in state.get("customer_order_lines"):
        line_id = line.get("customer_order_line_id", line.get("id", ""))
        if customer_order_line_ids is not None and line_id not in customer_order_line_ids:
            continue
        link = allocations.get(line_id, {})
        production_order_id = (
            line.get("production_order_id")
            or line.get("assigned_production_order_id")
            or link.get("production_order_id")
            or link.get("assigned_production_order_id", "")
        )
        if production_order_ids is not None and production_order_id not in production_order_ids:
            continue
        customer_order_id = line.get("customer_order_id", "")
        order = orders.get(customer_order_id, {})
        promised_value = order.get("promised_delivery_time")
        promised = parse_time(promised_value) if promised_value else None
        unit_revenue = Decimal(line["unit_revenue"]) if line.get("unit_revenue") else None
        open_quantity = max(
            Decimal("0"),
            Decimal(line.get("ordered_quantity", "0"))
            - Decimal(line.get("fulfilled_quantity", "0")),
        )
        quality = "COMPLETE"
        if promised is None:
            quality = "PARTIAL_CRITICAL"
        impact = production_by_id.get(production_order_id)
        segments: list[FulfilmentSegment] = []
        if impact is not None:
            remaining = open_quantity
            for batch in impact.batches:
                if batch.projected_completion is None or remaining <= 0:
                    continue
                quantity = min(remaining, batch.quantity)
                availability = batch.projected_completion
                delivery = _delivery_time(availability)
                if availability <= horizon.simulation_end_time:
                    segments.append(
                        FulfilmentSegment(
                            order_line_id=line_id,
                            quantity=quantity,
                            availability_time=availability,
                            projected_delivery=delivery,
                            production_batch_id=batch.batch_id,
                            facility_id=batch.facility_id,
                        )
                    )
                    remaining -= quantity
        result.append(
            CustomerImpact(
                customer_order_id=customer_order_id,
                customer_order_line_id=line_id,
                production_order_id=production_order_id,
                product_id=line.get("product_id", ""),
                open_quantity=open_quantity,
                promised_delivery=promised,
                unit_revenue=unit_revenue,
                segments=tuple(segments),
                data_quality_status=quality,
            )
        )
    return tuple(sorted(result, key=lambda item: item.customer_order_line_id))
