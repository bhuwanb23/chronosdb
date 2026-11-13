from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "purchase_order_id": self.purchase_order_id,
            "warehouse_id": self.warehouse_id,
            "component_id": self.component_id,
            "quantity": str(self.quantity),
            "event_time": self.event_time.isoformat().replace("+00:00", "Z"),
            "event_type": self.event_type,
            "source": self.source,
            "original_event_time": self.original_event_time.isoformat().replace("+00:00", "Z"),
            "within_horizon": self.within_horizon,
            "rule_id": self.rule_id,
        }
