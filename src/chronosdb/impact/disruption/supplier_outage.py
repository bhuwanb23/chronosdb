from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from ..contracts.errors import DisruptionValidationError
from ..contracts.requests import parse_time
from ..state.reconstruction import OperationalState


def _utc_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class Disruption:
    event_id: str
    event_type: str
    supplier_id: str
    start_time: datetime
    end_time: datetime
    recovery_lag: timedelta
    scope_type: str
    component_ids: frozenset[str] = frozenset()
    purchase_order_ids: frozenset[str] = frozenset()

    @classmethod
    def from_state(cls, state: OperationalState, event_id: str) -> Disruption:
        event = next(
            (
                row
                for row in state.get("disruption_events")
                if row["disruption_event_id"] == event_id
            ),
            None,
        )
        if event is None:
            raise DisruptionValidationError(f"unknown disruption event: {event_id}")
        component_ids = frozenset(
            row["component_id"]
            for row in state.get("disruption_scope_components")
            if row["disruption_event_id"] == event_id
        )
        purchase_order_ids = frozenset(
            row["purchase_order_id"]
            for row in state.get("disruption_scope_purchase_orders")
            if row["disruption_event_id"] == event_id
        )
        start = parse_time(event["start_time"])
        end = parse_time(event["expected_end_time"])
        if end <= start:
            raise DisruptionValidationError("disruption end must be after start")
        return cls(
            event_id=event_id,
            event_type=event["event_type"],
            supplier_id=event["supplier_id"],
            start_time=start,
            end_time=end,
            recovery_lag=timedelta(hours=int(event["recovery_lag_hours"])),
            scope_type=event["scope_type"],
            component_ids=component_ids,
            purchase_order_ids=purchase_order_ids,
        )


@dataclass(frozen=True)
class PurchaseOrderImpact:
    purchase_order_id: str
    supplier_id: str
    component_id: str
    warehouse_id: str
    outstanding_quantity: Decimal
    original_arrival: datetime
    disrupted_arrival: datetime
    delay_hours: int
    rule_id: str
    source_record_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "purchase_order_id": self.purchase_order_id,
            "supplier_id": self.supplier_id,
            "component_id": self.component_id,
            "warehouse_id": self.warehouse_id,
            "outstanding_quantity": str(self.outstanding_quantity),
            "original_arrival": _utc_iso(self.original_arrival),
            "disrupted_arrival": _utc_iso(self.disrupted_arrival),
            "delay_hours": self.delay_hours,
            "rule_id": self.rule_id,
            "source_record_ids": list(self.source_record_ids),
        }


def resolve_purchase_order_impacts(
    state: OperationalState, disruption: Disruption
) -> tuple[PurchaseOrderImpact, ...]:
    impacts: list[PurchaseOrderImpact] = []
    for order in state.get("purchase_orders"):
        if order.get("supplier_id") != disruption.supplier_id:
            continue
        if order.get("status", "").upper() in {"RECEIVED", "CANCELLED", "CLOSED"}:
            continue
        outstanding = max(
            Decimal("0"),
            Decimal(order.get("ordered_quantity", "0"))
            - Decimal(order.get("received_quantity", "0")),
        )
        if outstanding <= 0:
            continue
        original = parse_time(order["expected_arrival_time"])
        if original < disruption.start_time:
            continue
        if disruption.scope_type == "COMPONENT" and (
            order.get("component_id") not in disruption.component_ids
        ):
            continue
        if disruption.scope_type == "PURCHASE_ORDER" and (
            order.get("id") not in disruption.purchase_order_ids
        ):
            continue
        disrupted = max(original, disruption.end_time + disruption.recovery_lag)
        delay = int((disrupted - original).total_seconds() // 3600)
        impacts.append(
            PurchaseOrderImpact(
                purchase_order_id=order["id"],
                supplier_id=order["supplier_id"],
                component_id=order["component_id"],
                warehouse_id=order["destination_warehouse_id"],
                outstanding_quantity=outstanding,
                original_arrival=original,
                disrupted_arrival=disrupted,
                delay_hours=delay,
                rule_id="SUP-004",
                source_record_ids=(order["id"], disruption.event_id),
            )
        )
    return tuple(sorted(impacts, key=lambda item: item.purchase_order_id))
