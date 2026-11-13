12. Phase 5H: Inventory Timeline Engine
Goal

Build a chronological component balance for each relevant warehouse.

Timeline event types
Plain Text
OPENING_STATE
PURCHASE_RECEIPT
EXISTING_TRANSFER_IN
EXISTING_TRANSFER_OUT
PRODUCTION_ISSUE
PRODUCTION_RETURN
QUARANTINE
QUARANTINE_RELEASE
ADJUSTMENT
PROJECTED_CONSUMPTION

No recovery intervention is added in Phase 5.

Event ordering

When multiple events share a timestamp, use a documented precedence order.

Recommended:

Historical factual event
Opening or correction event
Receipt available at timestamp
Reservation release
Mandatory in-progress production issue
Released production issue
Planned production issue
Lower-priority consumption

Within the same class:

Priority
Required time
Stable record ID

The ordering must match the frozen ground truth.

Projected inventory equation
Balancet=Balancet−1+Receiptst+TransfersInt+Returnst+PositiveAdjustmentst−Consumptiont−TransfersOutt−Quarantinet−NegativeAdjustmentstBalance_t = Balance_{t-1} + Receipts_t + TransfersIn_t + Returns_t + PositiveAdjustments_t - Consumption_t - TransfersOut_t - Quarantine_t - NegativeAdjustments_tBalancet​=Balancet−1​+Receiptst​+TransfersInt​+Returnst​+PositiveAdjustmentst​−Consumptiont​−TransfersOutt​−Quarantinet​−NegativeAdjustmentst​
Safety stock

Track separately:

Plain Text
physical balance
available balance
safety-stock threshold
safety-stock breach
material shortage

Falling below safety stock is not automatically the same as insufficient production material.

Timeline output
JSON
{
"warehouse_id": "WH-PUNE",
"component_id": "CMP-MCU-42",
"opening_available": "400",
"events": [],
"minimum_balance": "0",
"first_safety_stock_breach": "...",
"first_material_shortage": "...",
"ending_balance": "..."
}
Sparse processing

Do not iterate over every hour if no event exists.

Use an event-driven timeline:

Plain Text
sort relevant event points
apply deltas
evaluate requirements at each event point

This improves performance while preserving exact results.

Inventory invariants
No receipt consumed before event time.
No component mixed across incompatible units.
Consumption is linked to production demand.
No unexplained inventory creation.
Opening plus events equals ending state.
A failed allocation does not push physical inventory negative.
Deliverables
Plain Text
src/backend/chronosdb/impact/inventory/
docs/impact-engine/inventory-timeline.md
