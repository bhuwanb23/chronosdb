from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

EVENT_PRECEDENCE: dict[str, int] = {
    "HISTORICAL_FACT": 10,
    "OPENING_STATE": 20,
    "PURCHASE_RECEIPT": 30,
    "PROJECTED_PURCHASE_RECEIPT": 30,
    "RESERVATION_RELEASE": 40,
    "MANDATORY_PRODUCTION_ISSUE": 50,
    "PRODUCTION_ISSUE": 60,
    "RELEASED_PRODUCTION_ISSUE": 60,
    "PLANNED_PRODUCTION_ISSUE": 70,
    "PROJECTED_CONSUMPTION": 80,
    "EXISTING_TRANSFER_IN": 90,
    "EXISTING_TRANSFER_OUT": 90,
    "PRODUCTION_RETURN": 90,
    "QUARANTINE": 90,
    "QUARANTINE_RELEASE": 90,
    "ADJUSTMENT": 90,
}


def utc_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class InventoryEvent:
    event_id: str
    event_time: datetime
    event_type: str
    warehouse_id: str
    component_id: str
    quantity: Decimal
    source_record_ids: tuple[str, ...] = ()
    reference_id: str | None = None
    priority: int = 0

    @property
    def precedence(self) -> int:
        return EVENT_PRECEDENCE.get(self.event_type, 999)

    @property
    def delta(self) -> Decimal:
        if self.event_type in {
            "PURCHASE_RECEIPT",
            "PROJECTED_PURCHASE_RECEIPT",
            "EXISTING_TRANSFER_IN",
            "PRODUCTION_RETURN",
            "QUARANTINE_RELEASE",
        }:
            return self.quantity
        if self.event_type in {
            "EXISTING_TRANSFER_OUT",
            "PRODUCTION_ISSUE",
            "RELEASED_PRODUCTION_ISSUE",
            "PLANNED_PRODUCTION_ISSUE",
            "PROJECTED_CONSUMPTION",
            "QUARANTINE",
        }:
            return -self.quantity
        if self.event_type == "ADJUSTMENT":
            return self.quantity
        return Decimal("0")

    def sort_key(self) -> tuple[datetime, int, int, str]:
        return (self.event_time, self.precedence, self.priority, self.event_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_time": utc_iso(self.event_time),
            "event_type": self.event_type,
            "warehouse_id": self.warehouse_id,
            "component_id": self.component_id,
            "quantity": str(self.quantity),
            "delta": str(self.delta),
            "reference_id": self.reference_id,
            "source_record_ids": list(self.source_record_ids),
        }
