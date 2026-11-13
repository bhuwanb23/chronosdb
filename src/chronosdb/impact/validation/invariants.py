from __future__ import annotations

from decimal import Decimal

from ..contracts.errors import ContractError


def require_non_negative_quantity(value: Decimal, field: str) -> None:
    if value < 0:
        raise ContractError(f"{field} cannot be negative")
