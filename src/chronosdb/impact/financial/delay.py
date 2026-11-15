from __future__ import annotations

from datetime import datetime


def calculate_delay_hours(
    projected_delivery: datetime | None,
    promised_delivery: datetime | None,
) -> int:
    """Return non-negative whole-hour delay between projected and promised delivery."""
    if projected_delivery is None or promised_delivery is None:
        return 0
    return max(0, int((projected_delivery - promised_delivery).total_seconds() // 3600))
