11. Phase 5G: Inbound-Supply Projection
Goal

Transform affected procurement commitments into deterministic future receipt events.

Receipt-event model
JSON
{
"event_id": "RCPT-PROJ-...",
"purchase_order_id": "PO-2208",
"warehouse_id": "WH-PUNE",
"component_id": "CMP-MCU-42",
"quantity": "800",
"event_time": "2026-11-27T00:00:00Z",
"event_type": "PROJECTED_PURCHASE_RECEIPT",
"source": "DISRUPTION_ADJUSTED",
"original_event_time": "2026-11-13T00:00:00Z"
}
Supply event rules
Received quantity remains historical fact.
Only outstanding quantity becomes projected receipt.
No receipt occurs twice.
A disrupted receipt replaces its original future receipt.
Projection does not update the operational purchase order.
A receipt beyond the horizon is retained as unresolved future supply but excluded from within-horizon availability.
Supply comparison

For each affected receipt:

Plain Text
Original event
Disrupted event
Time delta
Quantity delta
Availability-window effect
Supply-affected component

A component is supply affected if any eligible future receipt changes in time or quantity.

This remains distinct from shortage-affected component.

Deliverables
Plain Text
src/backend/chronosdb/impact/supply/projection.py
docs/impact-engine/inbound-supply-projection.md
