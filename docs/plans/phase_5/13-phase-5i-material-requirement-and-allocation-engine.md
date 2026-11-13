13. Phase 5I: Material Requirement and Allocation Engine
Goal

Determine how available component inventory is allocated to production demand.

Material-requirement calculation

For remaining production quantity:

GrossRequirementp,c=RemainingQuantityp×BOMQuantityp,c×(1+ScrapFactorp,c)GrossRequirement_{p,c} = RemainingQuantity_p \times BOMQuantity_{p,c} \times (1 + ScrapFactor_{p,c})GrossRequirementp,c​=RemainingQuantityp​×BOMQuantityp,c​×(1+ScrapFactorp,c​)

For discrete components:

RequiredQuantityp,c=⌈GrossRequirementp,c⌉RequiredQuantity_{p,c} = \lceil GrossRequirement_{p,c} \rceilRequiredQuantityp,c​=⌈GrossRequirementp,c​⌉
Batch-level requirement

For the golden 100-unit batch:

100×2=200 MCU100 \times 2 = 200\ MCU100×2=200 MCU
BOM selection

Use BOM active at the planned production start unless the locked rule specifies projected-start selection.

The recommended frozen rule remains:

Select the BOM active at the production order's planned start.

Changing projected dates must not silently select a different BOM version.

Allocation priority
In-progress locked batches
Released production orders
Customer priority
Promised delivery
Production planned start
Production-order identifier
Batch identifier
Allocation result states
Plain Text
FULLY_ALLOCATED
PARTIALLY_ALLOCATED
UNALLOCATED
INSUFFICIENT_DATA
Allocation object
JSON
{
"production_order_id": "MO-0882",
"batch_id": "MO-0882-B01",
"component_id": "CMP-MCU-42",
"required_quantity": "200",
"allocated_quantity": "0",
"shortage_quantity": "200",
"required_time": "...",
"material_ready_time": "2026-11-27T00:00:00Z",
"source_lots": []
}
Reservation rule

Do not subtract reservations in the opening state and then allocate the same reserved demand again.

Implement one of these models consistently:

Preferred
Existing reservations are mapped to specific production obligations.
Their inventory remains allocated to those obligations.
Unreserved available inventory is allocated to remaining demand.
Deliverables
Plain Text
src/backend/chronosdb/impact/materials/
docs/impact-engine/material-allocation.md
Exit gate
Allocation is deterministic.
Materials are not double allocated.
BOM version is correct.
Partial production follows 100-unit batches for the golden scenario.
Allocation provenance identifies source inventory and receipts.
