from __future__ import annotations

from decimal import Decimal
from typing import Any


def monetary_payload(value: Decimal | None, currency: str = "INR") -> dict[str, Any]:
    return {
        "amount": f"{(value or Decimal('0')):.2f}",
        "currency": currency,
    }
