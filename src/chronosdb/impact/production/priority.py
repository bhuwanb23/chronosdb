from __future__ import annotations

from typing import Any


def scheduling_priority(requirement: Any) -> tuple[Any, ...]:
    """Stable scheduling order: order priority, customer priority, start, IDs."""
    return (
        requirement.order_priority,
        requirement.customer_priority,
        requirement.planned_start,
        requirement.production_order_id,
        requirement.batch_id,
    )
