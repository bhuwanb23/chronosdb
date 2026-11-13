14. Phase 5J: Shortage Detection Engine
Goal

Identify when production demand cannot be met and quantify the shortfall.

Shortage definition

A shortage occurs when eligible quantity at the required time is less than requirement.

ShortageQuantity=max⁡(0,RequiredQuantity−EligibleQuantity)ShortageQuantity = \max( 0, RequiredQuantity - EligibleQuantity )ShortageQuantity=max(0,RequiredQuantity−EligibleQuantity)
Shortage types
Plain Text
TEMPORARY_SHORTAGE
HORIZON_SHORTAGE
PARTIAL_SHORTAGE
MISSING_DATA
Temporary shortage

Supply arrives later within the horizon.

Horizon shortage

Supply does not become available within the horizon.

Partial shortage

Some but not all requirement can be allocated.

Missing data

The quantity cannot be calculated because a critical record is absent.

Required outputs
Plain Text
component_id
warehouse_id
production_order_id
batch_id
required_time
required_quantity
available_quantity
shortage_quantity
resolved_time
source_receipt_id
causal_parent_ids
First shortage versus aggregate shortage

Report both:

Earliest shortage timestamp
Maximum simultaneous shortage
Total unmet quantity by order
Shortage-resolution timestamp

Do not sum the same rolling shortage repeatedly across timeline points.

Deliverables
Plain Text
src/backend/chronosdb/impact/inventory/shortage.py
docs/impact-engine/shortage-calculation.md
