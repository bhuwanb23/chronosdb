from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from .events import utc_iso


class ShortageType(StrEnum):
    TEMPORARY_SHORTAGE = "TEMPORARY_SHORTAGE"
    HORIZON_SHORTAGE = "HORIZON_SHORTAGE"
    PARTIAL_SHORTAGE = "PARTIAL_SHORTAGE"
    MISSING_DATA = "MISSING_DATA"


@dataclass(frozen=True)
class Shortage:
    component_id: str
    warehouse_id: str
    production_order_id: str
    batch_id: str
    required_time: datetime
    required_quantity: Decimal
    available_quantity: Decimal
    shortage_quantity: Decimal
    shortage_type: ShortageType
    resolved_time: datetime | None
    source_receipt_id: str | None
    causal_parent_ids: tuple[str, ...]
    rule_id: str = "INV-003"

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "warehouse_id": self.warehouse_id,
            "production_order_id": self.production_order_id,
            "batch_id": self.batch_id,
            "required_time": utc_iso(self.required_time),
            "required_quantity": str(self.required_quantity),
            "available_quantity": str(self.available_quantity),
            "shortage_quantity": str(self.shortage_quantity),
            "shortage_type": self.shortage_type.value,
            "resolved_time": utc_iso(self.resolved_time) if self.resolved_time else None,
            "source_receipt_id": self.source_receipt_id,
            "causal_parent_ids": list(self.causal_parent_ids),
            "rule_id": self.rule_id,
        }


def _get(value: Any, name: str, default: Any = None) -> Any:
    return value.get(name, default) if isinstance(value, dict) else getattr(value, name, default)


def detect_shortages(
    allocations: Iterable[Any],
    horizon_end: datetime | None = None,
) -> tuple[Shortage, ...]:
    """Convert allocation deficits to one stable record per requirement."""
    shortages: list[Shortage] = []
    for allocation in allocations:
        required = Decimal(str(_get(allocation, "required_quantity", "0")))
        available = Decimal(str(_get(allocation, "allocated_quantity", "0")))
        shortage_quantity = max(Decimal("0"), required - available)
        if shortage_quantity <= 0:
            continue
        required_time = _get(allocation, "required_time")
        if required_time is None:
            continue
        resolved_time = _get(allocation, "material_ready_time")
        if resolved_time is not None and horizon_end is not None and resolved_time <= horizon_end:
            shortage_type = (
                ShortageType.PARTIAL_SHORTAGE
                if available > 0
                else ShortageType.TEMPORARY_SHORTAGE
            )
        else:
            shortage_type = ShortageType.HORIZON_SHORTAGE
        source_lots = _get(allocation, "source_lots", ()) or ()
        source_receipt_id = None
        if source_lots:
            first_lot = source_lots[0]
            source_receipt_id = (
                first_lot.get("source_id")
                if isinstance(first_lot, dict)
                else getattr(first_lot, "source_id", None)
            )
        parent_ids = tuple(_get(allocation, "causal_parent_ids", ()) or ())
        shortages.append(
            Shortage(
                component_id=str(_get(allocation, "component_id", "")),
                warehouse_id=str(_get(allocation, "warehouse_id", "")),
                production_order_id=str(_get(allocation, "production_order_id", "")),
                batch_id=str(_get(allocation, "batch_id", "")),
                required_time=required_time,
                required_quantity=required,
                available_quantity=available,
                shortage_quantity=shortage_quantity,
                shortage_type=shortage_type,
                resolved_time=resolved_time,
                source_receipt_id=source_receipt_id,
                causal_parent_ids=parent_ids,
            )
        )
    return tuple(
        sorted(
            shortages,
            key=lambda item: (
                item.required_time,
                item.component_id,
                item.production_order_id,
                item.batch_id,
            ),
        )
    )
