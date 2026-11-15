from __future__ import annotations

from decimal import ROUND_CEILING, Decimal


def batch_count(remaining_quantity: Decimal, batch_size: Decimal) -> int:
    """Number of production batches needed for the remaining quantity."""
    if batch_size <= 0:
        return 0
    return int((remaining_quantity / batch_size).to_integral_value(rounding=ROUND_CEILING))


def batch_id(production_order_id: str, index: int) -> str:
    """Stable batch identifier used by the scheduler and inventory ledger."""
    return f"{production_order_id}-B{index + 1:02d}"


def batch_quantity(
    remaining_quantity: Decimal,
    batch_size: Decimal,
    index: int,
) -> Decimal:
    return min(batch_size, remaining_quantity - (Decimal(index) * batch_size))
