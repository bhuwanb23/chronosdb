11. Phase 4G: Manufacturing-Data Production
Goal

Create production orders whose material requirements, capacity usage, and customer commitments reconcile.

Production-order fields
Plain Text
production_order_id
product_id
facility_id
planned_quantity
completed_quantity
planned_start_time
planned_completion_time
actual_start_time
actual_completion_time
priority
status
batch_size
Material requirements

For production order ppp and component ccc:

Requiredp,c=⌈RemainingProductionQuantityp×BOMQuantityp,c×(1+ScrapFactorp,c)⌉Required_{p,c} = \left\lceil RemainingProductionQuantity_p \times BOMQuantity_{p,c} \times (1 + ScrapFactor_{p,c}) \right\rceilRequiredp,c​=⌈RemainingProductionQuantityp​×BOMQuantityp,c​×(1+ScrapFactorp,c​)⌉
Required production patterns

Include:

Completed orders
In-progress orders
Released orders
Planned orders
Material-blocked orders
Capacity-delayed orders
High-priority customer-linked orders
Capacity generation

Facility capacity must be represented as a calendar:

Plain Text
facility_id
date_or_interval
available_capacity
reserved_capacity
maintenance_capacity
effective_capacity
Capacity invariant

For each facility and interval:

AllocatedCapacity≤EffectiveCapacityAllocatedCapacity \leq EffectiveCapacityAllocatedCapacity≤EffectiveCapacity
Golden production orders
Order	Product qty.	MCU requirement	Planned interval
MO-0876	200	400	12–14 Nov
MO-0882	200	400	15–17 Nov
MO-0889	200	400	18–20 Nov

Facility:

Plain Text
FAC-PUNE
Capacity: 100 products per calendar day
Batch size: 100 products
Material-consumption convention

Lock this rule:

Material for each 100-unit batch is consumed at batch start.

Therefore, each batch of PRD-CONTROLLER-X consumes:

100×2=200 MCU units100 \times 2 = 200\ \text{MCU units}100×2=200 MCU units
Deliverables
Plain Text
data/releases/v1.0.0/production/
├── production_orders.csv
├── production_order_status_history.csv
├── production_batches.csv
├── production_material_requirements.csv
├── production_material_allocations.csv
└── facility_capacity_calendar.csv
