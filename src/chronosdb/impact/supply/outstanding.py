from __future__ import annotations

from decimal import Decimal


def outstanding_quantity(ordered_quantity: str, received_quantity: str) -> Decimal:
    return max(
        Decimal("0"),
        Decimal(ordered_quantity) - Decimal(received_quantity),
    )
