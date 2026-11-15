from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal

from ..contracts.requests import SimulationHorizon
from ..state.reconstruction import OperationalState


def capacity_map(state: OperationalState) -> dict[tuple[str, str], Decimal]:
    return {
        (row.get("facility_id", ""), row.get("capacity_date", "")): Decimal(
            row.get(
                "available_capacity",
                str(
                    Decimal(row.get("effective_capacity", "0"))
                    - Decimal(row.get("reserved_capacity", "0"))
                    - Decimal(row.get("maintenance_capacity", "0"))
                ),
            )
        )
        for row in state.get("facility_capacity_calendar")
    }


def new_capacity_usage() -> dict[tuple[str, str], Decimal]:
    return defaultdict(Decimal)


def find_capacity_time(
    facility_id: str,
    start: datetime,
    quantity: Decimal,
    capacity: dict[tuple[str, str], Decimal],
    used: dict[tuple[str, str], Decimal],
    horizon: SimulationHorizon,
) -> datetime | None:
    candidate = start
    while candidate <= horizon.simulation_end_time:
        date_key = candidate.date().isoformat()
        effective = capacity.get((facility_id, date_key), Decimal("0"))
        if effective - used[(facility_id, date_key)] >= quantity:
            return candidate
        candidate += timedelta(days=1)
    return None
