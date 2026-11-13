from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from ..contracts.requests import SimulationHorizon, parse_time
from ..state.reconstruction import OperationalState
from .events import InventoryEvent, utc_iso


def _decimal(value: str | int | Decimal | None) -> Decimal:
    return Decimal(str(value or "0"))


def _receipt_value(receipt: Any, name: str) -> Any:
    if isinstance(receipt, dict):
        return receipt.get(name)
    return getattr(receipt, name)


@dataclass(frozen=True)
class InventoryTimeline:
    warehouse_id: str
    component_id: str
    opening_time: datetime
    opening_physical: Decimal
    opening_available: Decimal
    safety_stock: Decimal
    events: tuple[InventoryEvent, ...]
    minimum_balance: Decimal
    first_safety_stock_breach: datetime | None
    first_material_shortage: datetime | None
    ending_balance: Decimal
    ending_available: Decimal

    def to_dict(self) -> dict[str, Any]:
        return {
            "warehouse_id": self.warehouse_id,
            "component_id": self.component_id,
            "opening_time": utc_iso(self.opening_time),
            "opening_physical": str(self.opening_physical),
            "opening_available": str(self.opening_available),
            "safety_stock": str(self.safety_stock),
            "events": [event.to_dict() for event in self.events],
            "minimum_balance": str(self.minimum_balance),
            "first_safety_stock_breach": (
                utc_iso(self.first_safety_stock_breach)
                if self.first_safety_stock_breach is not None
                else None
            ),
            "first_material_shortage": (
                utc_iso(self.first_material_shortage)
                if self.first_material_shortage is not None
                else None
            ),
            "ending_balance": str(self.ending_balance),
            "ending_available": str(self.ending_available),
        }

    def with_shortage_time(self, shortage_time: datetime | None) -> InventoryTimeline:
        return replace(self, first_material_shortage=shortage_time)


def _event_from_transaction(row: dict[str, str]) -> InventoryEvent | None:
    event_type = row.get("transaction_type", "").upper()
    if event_type == "OPENING_BALANCE":
        return None
    mapping = {
        "PURCHASE_RECEIPT": "PURCHASE_RECEIPT",
        "EXISTING_TRANSFER_IN": "EXISTING_TRANSFER_IN",
        "EXISTING_TRANSFER_OUT": "EXISTING_TRANSFER_OUT",
        "PRODUCTION_ISSUE": "PRODUCTION_ISSUE",
        "PRODUCTION_RETURN": "PRODUCTION_RETURN",
        "QUARANTINE": "QUARANTINE",
        "QUARANTINE_RELEASE": "QUARANTINE_RELEASE",
        "ADJUSTMENT": "ADJUSTMENT",
    }
    normalized = mapping.get(event_type)
    if normalized is None or not row.get("event_time"):
        return None
    return InventoryEvent(
        event_id=row.get("id", ""),
        event_time=parse_time(row["event_time"]),
        event_type=normalized,
        warehouse_id=row.get("warehouse_id", ""),
        component_id=row.get("component_id", ""),
        quantity=_decimal(row.get("quantity")),
        reference_id=row.get("reference_id") or None,
        source_record_ids=(row.get("id", ""),),
    )


def _events_from_transfer(row: dict[str, str]) -> tuple[InventoryEvent, ...]:
    if not row.get("event_time"):
        return ()
    event_time = parse_time(row["event_time"])
    quantity = _decimal(row.get("quantity"))
    transfer_id = row.get("transfer_id", row.get("id", ""))
    source_ids = (row.get("id", ""), transfer_id)
    return (
        InventoryEvent(
            event_id=f"{row.get('id', '')}-OUT",
            event_time=event_time,
            event_type="EXISTING_TRANSFER_OUT",
            warehouse_id=row.get("source_warehouse_id", ""),
            component_id=row.get("component_id", ""),
            quantity=quantity,
            reference_id=transfer_id,
            source_record_ids=source_ids,
        ),
        InventoryEvent(
            event_id=f"{row.get('id', '')}-IN",
            event_time=event_time,
            event_type="EXISTING_TRANSFER_IN",
            warehouse_id=row.get("destination_warehouse_id", ""),
            component_id=row.get("component_id", ""),
            quantity=quantity,
            reference_id=transfer_id,
            source_record_ids=source_ids,
        ),
    )


def _timeline(
    warehouse_id: str,
    component_id: str,
    opening: dict[str, str],
    events: Iterable[InventoryEvent],
) -> InventoryTimeline:
    opening_physical = _decimal(opening.get("on_hand_quantity"))
    opening_available = max(
        Decimal("0"),
        opening_physical
        - _decimal(opening.get("quarantined_quantity"))
        - _decimal(opening.get("reserved_quantity")),
    )
    safety_stock = _decimal(opening.get("safety_stock_quantity"))
    ordered = tuple(sorted(events, key=lambda event: event.sort_key()))
    physical = opening_physical
    available = opening_available
    minimum = physical
    first_safety: datetime | None = None
    for event in ordered:
        physical += event.delta
        available += event.delta
        if physical < 0:
            raise ValueError(f"inventory balance became negative at {event.event_id}")
        minimum = min(minimum, physical)
        if first_safety is None and available < safety_stock:
            first_safety = event.event_time
    return InventoryTimeline(
        warehouse_id=warehouse_id,
        component_id=component_id,
        opening_time=parse_time(
            opening.get("snapshot_time", "1970-01-01T00:00:00Z")
        ),
        opening_physical=opening_physical,
        opening_available=opening_available,
        safety_stock=safety_stock,
        events=ordered,
        minimum_balance=minimum,
        first_safety_stock_breach=first_safety,
        first_material_shortage=None,
        ending_balance=physical,
        ending_available=available,
    )


def build_inventory_timelines(
    state: OperationalState,
    horizon: SimulationHorizon,
    projected_receipts: Iterable[Any] = (),
    projected_consumption: Iterable[InventoryEvent] = (),
) -> tuple[InventoryTimeline, ...]:
    """Build sparse, deterministic balances for every opening inventory position."""
    openings = {
        (row.get("warehouse_id", ""), row.get("component_id", "")): row
        for row in state.get("inventory_opening_balances")
    }
    events_by_key: dict[tuple[str, str], list[InventoryEvent]] = {}
    for row in state.get("inventory_transactions"):
        event = _event_from_transaction(row)
        if event is not None and event.event_time <= horizon.simulation_end_time:
            events_by_key.setdefault((event.warehouse_id, event.component_id), []).append(event)
    for row in state.get("transfer_transactions"):
        for event in _events_from_transfer(row):
            if horizon.as_of_time <= event.event_time <= horizon.simulation_end_time:
                events_by_key.setdefault((event.warehouse_id, event.component_id), []).append(
                    event
                )
    for receipt in projected_receipts:
        event_time = _receipt_value(receipt, "event_time")
        if isinstance(event_time, str):
            event_time = parse_time(event_time)
        if (
            event_time is None
            or event_time < horizon.as_of_time
            or event_time > horizon.simulation_end_time
            or not _receipt_value(receipt, "within_horizon")
        ):
            continue
        event = InventoryEvent(
            event_id=str(_receipt_value(receipt, "event_id")),
            event_time=event_time.astimezone(UTC),
            event_type="PROJECTED_PURCHASE_RECEIPT",
            warehouse_id=str(_receipt_value(receipt, "warehouse_id")),
            component_id=str(_receipt_value(receipt, "component_id")),
            quantity=_decimal(_receipt_value(receipt, "quantity")),
            reference_id=str(_receipt_value(receipt, "purchase_order_id")),
            source_record_ids=tuple(_receipt_value(receipt, "source_record_ids")),
        )
        events_by_key.setdefault((event.warehouse_id, event.component_id), []).append(event)
    for event in projected_consumption:
        if horizon.as_of_time <= event.event_time <= horizon.simulation_end_time:
            events_by_key.setdefault((event.warehouse_id, event.component_id), []).append(event)
    timelines: list[InventoryTimeline] = []
    for key, opening in openings.items():
        timelines.append(_timeline(key[0], key[1], opening, events_by_key.get(key, ())))
    return tuple(
        sorted(
            timelines,
            key=lambda timeline: (timeline.warehouse_id, timeline.component_id),
        )
    )
