"""Phase 4J disruption events, scopes, and status history."""

from __future__ import annotations

from typing import Any

from .release_export import write_release_csv
from .release_profile import ReleaseProfile, release_root


def build_disruptions(
    profile: ReleaseProfile,
    procurement: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Create scoped disruption events without mutating source operations."""
    purchase_orders = procurement["purchase_orders"]
    golden_event = {
        "disruption_event_id": "EVT-GOLD-001",
        "event_type": "SUPPLIER_OUTAGE",
        "supplier_id": "SUP-0104",
        "start_time": "2026-11-11T02:30:00Z",
        "expected_end_time": "2026-11-25T02:30:00Z",
        "reported_time": "2026-11-11T03:00:00Z",
        "scope_type": "ALL_SUPPLY",
        "severity": "CRITICAL",
        "recovery_lag_hours": "48",
        "projected_arrival_time": "2026-11-27T02:30:00Z",
        "status": "ACTIVE",
    }
    events = [golden_event]
    event_types = (
        "PARTIAL_SUPPLY_INTERRUPTION",
        "SHIPMENT_DELAY",
        "QUALITY_HOLD",
    )
    for index, event_type in enumerate(event_types, start=1):
        order = purchase_orders[index]
        events.append(
            {
                "disruption_event_id": f"EVT-P4-{index:04d}",
                "event_type": event_type,
                "supplier_id": order["supplier_id"],
                "start_time": order["order_time"],
                "expected_end_time": order["expected_arrival_time"],
                "reported_time": order["order_time"],
                "scope_type": (
                    "COMPONENT"
                    if event_type != "SHIPMENT_DELAY"
                    else "PURCHASE_ORDER"
                ),
                "severity": "HIGH" if event_type != "QUALITY_HOLD" else "MEDIUM",
                "recovery_lag_hours": str(24 + index * 12),
                "projected_arrival_time": order["expected_arrival_time"],
                "status": "CLOSED" if order["received_quantity"] != "0" else "ACTIVE",
            }
        )
    scope_components = [
        {
            "id": "EVSCOPE-GOLD-CMP",
            "disruption_event_id": "EVT-GOLD-001",
            "component_id": "CMP-MCU-42",
            "scope_reason": "ALL_SUPPLY",
        }
    ]
    scope_pos = [
        {
            "id": "EVSCOPE-GOLD-PO",
            "disruption_event_id": "EVT-GOLD-001",
            "purchase_order_id": "PO-2208",
            "scope_reason": "SUPPLIER_AND_COMPONENT_MATCH",
        }
    ]
    for index, event in enumerate(events[1:], start=1):
        order = purchase_orders[index]
        if event["scope_type"] == "COMPONENT":
            scope_components.append(
                {
                    "id": f"EVSCOPE-P4-CMP-{index:04d}",
                    "disruption_event_id": event["disruption_event_id"],
                    "component_id": order["component_id"],
                    "scope_reason": "COMPONENT_MATCH",
                }
            )
        else:
            scope_pos.append(
                {
                    "id": f"EVSCOPE-P4-PO-{index:04d}",
                    "disruption_event_id": event["disruption_event_id"],
                    "purchase_order_id": order["id"],
                    "scope_reason": "PURCHASE_ORDER_MATCH",
                }
            )
    status_history = []
    for event in events:
        status_history.extend(
            [
                {
                    "id": f"EVSTATUS-{event['disruption_event_id']}-01",
                    "disruption_event_id": event["disruption_event_id"],
                    "status": "REPORTED",
                    "event_time": event["reported_time"],
                    "recorded_at": event["reported_time"],
                },
                {
                    "id": f"EVSTATUS-{event['disruption_event_id']}-02",
                    "disruption_event_id": event["disruption_event_id"],
                    "status": event["status"],
                    "event_time": event["start_time"],
                    "recorded_at": event["reported_time"],
                },
            ]
        )
    output = release_root(profile) / "disruptions"
    write_release_csv(output / "disruption_events.csv", events)
    write_release_csv(output / "disruption_scope_components.csv", scope_components)
    write_release_csv(output / "disruption_scope_purchase_orders.csv", scope_pos)
    write_release_csv(output / "disruption_status_history.csv", status_history)
    return {
        "events": events,
        "scope_components": scope_components,
        "scope_purchase_orders": scope_pos,
        "status_history": status_history,
    }
