14. Phase 4J: Disruption-Event Production
Goal

Create realistic supplier events that affect only the intended supply.

Event fields
Plain Text
disruption_event_id
event_type
supplier_id
start_time
expected_end_time
reported_time
scope_type
affected_component_ids
affected_purchase_order_ids
severity
recovery_lag_hours
status
Event types in the release

The core dataset may include historical examples of:

Plain Text
SUPPLIER_OUTAGE
PARTIAL_SUPPLY_INTERRUPTION
SHIPMENT_DELAY
QUALITY_HOLD

The application MVP remains focused on SUPPLIER_OUTAGE.

Golden disruption
Plain Text
Event ID: EVT-GOLD-001
Type: SUPPLIER_OUTAGE
Supplier: SUP-0104
Scope: ALL_SUPPLY
Start: 11 Nov 2026, 08:00 IST
Duration: 14 days
End: 25 Nov 2026, 08:00 IST
Recovery lag: 48 hours
Affected purchase order: PO-2208
Resulting arrival
NewArrival=25 Nov+2 days=27 NovNewArrival = 25\ Nov + 2\ days = 27\ NovNewArrival=25 Nov+2 days=27 Nov
Event validation

A supplier event must not affect:

Received purchase-order quantity
Purchase orders before event scope
Other suppliers
Unlisted components in component-specific events
Cancelled purchase orders
Supply outside defined event rules
Deliverables
Plain Text
data/releases/v1.0.0/disruptions/
├── disruption_events.csv
├── disruption_scope_components.csv
├── disruption_scope_purchase_orders.csv
└── disruption_status_history.csv
