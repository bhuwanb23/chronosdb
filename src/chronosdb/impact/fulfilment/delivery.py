from __future__ import annotations

from datetime import UTC, datetime, time, timedelta
from typing import Any


def projected_delivery(
    availability_time: datetime,
    lead_days: int = 1,
) -> datetime:
    """Convert product availability into a delivery date at UTC midnight."""
    return datetime.combine(
        availability_time.date() + timedelta(days=lead_days),
        time.min,
        tzinfo=UTC,
    )


def baseline_deliveries(production_impacts: Any) -> dict[str, datetime]:
    """Return planned delivery dates for production orders before disruption."""
    result: dict[str, datetime] = {}
    for impact in production_impacts:
        planned_completion = getattr(impact, "planned_completion", None)
        if planned_completion is not None:
            result[impact.production_order_id] = projected_delivery(planned_completion)
    return result
