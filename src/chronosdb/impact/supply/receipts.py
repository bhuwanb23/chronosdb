from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any


def _utc_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class ProjectedReceipt:
    event_id: str
    purchase_order_id: str
    warehouse_id: str
    component_id: str
    quantity: Decimal
    event_time: datetime
    event_type: str
    source: str
    original_event_time: datetime
    within_horizon: bool
    rule_id: str
    source_record_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "purchase_order_id": self.purchase_order_id,
            "warehouse_id": self.warehouse_id,
            "component_id": self.component_id,
            "quantity": str(self.quantity),
            "event_time": _utc_iso(self.event_time),
            "event_type": self.event_type,
            "source": self.source,
            "original_event_time": _utc_iso(self.original_event_time),
            "within_horizon": self.within_horizon,
            "rule_id": self.rule_id,
            "source_record_ids": list(self.source_record_ids),
        }
