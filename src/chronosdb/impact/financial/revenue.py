from __future__ import annotations

from decimal import Decimal


def calculate_revenue_at_risk(
    late_quantity: Decimal,
    unit_revenue: Decimal | None,
) -> Decimal | None:
    """Revenue exposure is late quantity only, never on-time quantity."""
    if unit_revenue is None:
        return None
    return max(Decimal("0"), late_quantity) * unit_revenue


def revenue_bounds(
    revenue_at_risk: Decimal | None,
    open_quantity: Decimal,
    unit_revenue: Decimal | None,
) -> bool:
    """Verify 0 <= revenue_at_risk <= open_quantity * unit_revenue."""
    if revenue_at_risk is None or unit_revenue is None:
        return revenue_at_risk is None
    return Decimal("0") <= revenue_at_risk <= open_quantity * unit_revenue
