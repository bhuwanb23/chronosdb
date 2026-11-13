from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from .allocation import CustomerImpact


def _iso(value: datetime | None) -> str | None:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z") if value else None


@dataclass(frozen=True)
class SLAResult:
    customer_order_id: str
    customer_order_line_id: str
    production_order_id: str
    status: str
    open_quantity: Decimal
    on_time_quantity: Decimal
    late_quantity: Decimal
    projected_delivery: datetime | None
    promised_delivery: datetime | None
    delay_hours: int
    unit_revenue: Decimal | None
    revenue_at_risk: Decimal | None
    segments: tuple[dict[str, Any], ...]
    attribution: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_order_id": self.customer_order_id,
            "customer_order_line_id": self.customer_order_line_id,
            "production_order_id": self.production_order_id,
            "status": self.status,
            "open_quantity": str(self.open_quantity),
            "on_time_quantity": str(self.on_time_quantity),
            "late_quantity": str(self.late_quantity),
            "projected_delivery": _iso(self.projected_delivery),
            "promised_delivery": _iso(self.promised_delivery),
            "delay_hours": self.delay_hours,
            "unit_revenue": str(self.unit_revenue) if self.unit_revenue is not None else None,
            "revenue_at_risk": (
                str(self.revenue_at_risk) if self.revenue_at_risk is not None else None
            ),
            "segments": list(self.segments),
            "attribution": self.attribution,
        }


def calculate_sla_and_financial_impact(
    customer_impacts: tuple[CustomerImpact, ...],
    *,
    disruption_caused_production_order_ids: set[str] | None = None,
    horizon_end: datetime | None = None,
) -> tuple[tuple[SLAResult, ...], dict[str, Any]]:
    disruption_caused_production_order_ids = disruption_caused_production_order_ids or set()
    results: list[SLAResult] = []
    for impact in customer_impacts:
        segments = []
        for segment in impact.segments:
            segment_payload = segment.to_dict()
            if impact.promised_delivery is not None:
                segment_delay = max(
                    0,
                    int(
                        (
                            segment.projected_delivery - impact.promised_delivery
                        ).total_seconds()
                        // 3600
                    ),
                )
                segment_payload["delay_hours"] = segment_delay
                segment_payload["status"] = (
                    "BREACHED" if segment_delay > 0 else "ON_TIME"
                )
            segments.append(segment_payload)
        segments_tuple = tuple(segments)
        if impact.promised_delivery is None or impact.unit_revenue is None:
            results.append(
                SLAResult(
                    customer_order_id=impact.customer_order_id,
                    customer_order_line_id=impact.customer_order_line_id,
                    production_order_id=impact.production_order_id,
                    status="INSUFFICIENT_DATA",
                    open_quantity=impact.open_quantity,
                    on_time_quantity=Decimal("0"),
                    late_quantity=Decimal("0"),
                    projected_delivery=None,
                    promised_delivery=impact.promised_delivery,
                    delay_hours=0,
                    unit_revenue=impact.unit_revenue,
                    revenue_at_risk=None,
                    segments=segments_tuple,
                    attribution="INSUFFICIENT_EVIDENCE",
                )
            )
            continue
        projected_delivery = (
            max(segment.projected_delivery for segment in impact.segments)
            if impact.segments
            else None
        )
        on_time_quantity = sum(
            (
                segment.quantity
                for segment in impact.segments
                if segment.projected_delivery <= impact.promised_delivery
            ),
            Decimal("0"),
        )
        late_quantity = max(Decimal("0"), impact.open_quantity - on_time_quantity)
        delay_hours = (
            max(
                0,
                int(
                    (projected_delivery - impact.promised_delivery).total_seconds()
                    // 3600
                ),
            )
            if projected_delivery is not None
            else max(
                0,
                int(
                    ((horizon_end or impact.promised_delivery) - impact.promised_delivery)
                    .total_seconds()
                    // 3600
                ),
            )
        )
        status = "BREACHED" if late_quantity > 0 else "ON_TIME"
        results.append(
            SLAResult(
                customer_order_id=impact.customer_order_id,
                customer_order_line_id=impact.customer_order_line_id,
                production_order_id=impact.production_order_id,
                status=status,
                open_quantity=impact.open_quantity,
                on_time_quantity=on_time_quantity,
                late_quantity=late_quantity,
                projected_delivery=projected_delivery,
                promised_delivery=impact.promised_delivery,
                delay_hours=delay_hours,
                unit_revenue=impact.unit_revenue,
                revenue_at_risk=late_quantity * impact.unit_revenue,
                segments=segments_tuple,
                attribution=(
                    "DISRUPTION_CAUSED"
                    if (
                        status == "BREACHED"
                        and impact.production_order_id
                        in disruption_caused_production_order_ids
                    )
                    else "UNRELATED"
                ),
            )
        )
    late = [result for result in results if result.status == "BREACHED"]
    late_quantity = sum((item.late_quantity for item in results), Decimal("0"))
    revenue = sum(
        (item.revenue_at_risk or Decimal("0") for item in results),
        Decimal("0"),
    )
    total_delay_unit_hours = sum(
        (item.late_quantity * item.delay_hours for item in results),
        Decimal("0"),
    )
    metrics: dict[str, Any] = {
        "affected_supplier_count": 0,
        "affected_purchase_order_count": 0,
        "supply_affected_component_count": 0,
        "shortage_affected_component_count": 0,
        "affected_production_order_count": len(
            {item.production_order_id for item in results if item.late_quantity > 0}
        ),
        "affected_customer_order_count": len({item.customer_order_id for item in late}),
        "sla_breached_customer_order_count": len({item.customer_order_id for item in late}),
        "breached_customer_order_count": len({item.customer_order_id for item in late}),
        "breached_customer_order_line_count": len(late),
        "late_quantity": str(late_quantity),
        "total_delay_unit_hours": str(total_delay_unit_hours),
        "maximum_delay_hours": max((item.delay_hours for item in results), default=0),
        "average_delay_hours": (
            sum(item.delay_hours for item in late) / len(late) if late else 0
        ),
        "revenue_at_risk": {"amount": f"{revenue:.2f}", "currency": "INR"},
    }
    return tuple(results), metrics
