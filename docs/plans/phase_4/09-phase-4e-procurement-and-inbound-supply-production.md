9. Phase 4E: Procurement and Inbound-Supply Production
Goal

Create procurement records that are causally connected to component demand.

Purchase-order generation

Every purchase order must contain:

Plain Text
purchase_order_id
supplier_id
component_id
destination_warehouse_id
ordered_quantity
received_quantity
order_time
confirmed_time
expected_arrival_time
actual_arrival_time
status
unit_cost
currency
expedite_eligible
effective_state_time
Valid purchase-order states
Plain Text
DRAFT
CONFIRMED
IN_TRANSIT
PARTIALLY_RECEIVED
RECEIVED
DELAYED
CANCELLED
Quantity invariant
0≤ReceivedQuantity≤OrderedQuantity0 \leq ReceivedQuantity \leq OrderedQuantity0≤ReceivedQuantity≤OrderedQuantity
Outstanding quantity
OutstandingQuantity=max⁡(0,OrderedQuantity−ReceivedQuantity)OutstandingQuantity = \max(0, OrderedQuantity - ReceivedQuantity)OutstandingQuantity=max(0,OrderedQuantity−ReceivedQuantity)
Delivery behavior

The historical data should include:

Early arrivals
On-time arrivals
Minor delays
Major delays
Partial receipts
Cancelled orders

Recommended historical delivery distribution:

Outcome	Target share
On time	65–75%
Early	5–10%
1–3 days late	12–18%
More than 3 days late	5–10%
Cancelled or unresolved	1–3%

These are synthetic design targets, not claims about real suppliers.

Supplier-capacity validation

For generated alternate supply:

OrderQuantity≤AvailableCapacityOrderQuantity \leq AvailableCapacityOrderQuantity≤AvailableCapacity

If multiple purchase orders use the same supplier capacity window, aggregate them before validating.

Golden purchase order
Plain Text
PO-2208
Supplier: SUP-0104
Component: CMP-MCU-42
Quantity: 800 EA
Received: 0
Destination: WH-PUNE
Original arrival: 13 Nov 2026
Status before outage: CONFIRMED
Deliverables
Plain Text
data/releases/v1.0.0/operations/
├── purchase_orders.csv
├── purchase_order_status_history.csv
├── purchase_order_receipts.csv
└── supplier_capacity_calendar.csv
