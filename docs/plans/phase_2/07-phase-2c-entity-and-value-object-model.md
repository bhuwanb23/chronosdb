7. Phase 2C: Entity and Value-Object Model
Goal

Define the conceptual entities, identifiers, attributes and ownership boundaries.

7.1 Core entities
Supplier
Plain Text
supplier_id
supplier_name
status
region
effective_from
effective_to

Possible status:

Plain Text
ACTIVE
SUSPENDED
INACTIVE
Supplier-component agreement

Represents the approved relationship between a supplier and component.

Plain Text
supplier_component_id
supplier_id
component_id
approval_status
normal_lead_time_days
minimum_order_quantity
maximum_order_quantity
daily_capacity
unit_price
currency
effective_from
effective_to

Approval status:

Plain Text
APPROVED
CONDITIONAL
EXPIRED
REJECTED
Component
Plain Text
component_id
component_name
unit_of_measure
criticality
standard_unit_cost
currency
substitution_group
active_status
Product
Plain Text
product_id
product_name
unit_of_measure
standard_revenue_per_unit
currency
active_status
BOM version
Plain Text
bom_version_id
product_id
version_number
effective_from
effective_to
status
BOM line
Plain Text
bom_line_id
bom_version_id
component_id
quantity_per_product
scrap_factor
mandatory
Warehouse
Plain Text
warehouse_id
warehouse_name
region
status
Facility
Plain Text
facility_id
facility_name
region
status
daily_capacity_units
Inventory snapshot
Plain Text
inventory_snapshot_id
warehouse_id
component_id
snapshot_time
on_hand_quantity
reserved_quantity
quarantined_quantity
Purchase order
Plain Text
purchase_order_id
supplier_id
component_id
destination_warehouse_id
ordered_quantity
received_quantity
expected_arrival_time
status
unit_cost
expedite_eligible
Production order
Plain Text
production_order_id
product_id
facility_id
planned_quantity
completed_quantity
planned_start_time
planned_completion_time
priority
status
Production material allocation
Plain Text
allocation_id
production_order_id
component_id
warehouse_id
required_quantity
allocated_quantity
allocation_status
Customer order
Plain Text
customer_order_id
customer_id
order_time
promised_delivery_time
priority
sla_class
status
currency
Customer-order line
Plain Text
customer_order_line_id
customer_order_id
product_id
ordered_quantity
allocated_quantity
unit_revenue
production_order_id
Disruption event
Plain Text
disruption_event_id
event_type
supplier_id
start_time
expected_end_time
reported_time
status
scope
Scenario
Plain Text
scenario_id
as_of_time
disruption_event
objective
constraints
created_time
rule_version
status
Intervention
Plain Text
intervention_id
scenario_id
intervention_type
parameters
status
Simulation run
Plain Text
simulation_run_id
scenario_id
intervention_id
input_state_version
rule_version
started_at
completed_at
status
Decision result
Plain Text
decision_result_id
scenario_id
selected_intervention_id
objective
score
created_at
review_status
7.2 Value objects

Value objects do not possess independent business identity.

Examples:

Quantity
Money
Date interval
Lead time
Cost constraint
Service-level target
Optimization weights
Inventory position
Shortage result
Delay result
Evidence reference
Quantity
Plain Text
value
unit_of_measure

A quantity without a unit is invalid.

Money
Plain Text
amount
currency

Money values in different currencies cannot be added without an explicit conversion rule.

Effective interval
Plain Text
valid_from
valid_to

Use a half-open interval:

[valid_from,valid_to)[valid\_from, valid\_to)[valid_from,valid_to)

This avoids double-counting records at boundary timestamps.

Deliverable
Plain Text
docs/domain/conceptual-entity-model.md
Exit gate
Every entity has a stable identifier.
Attributes belong to the correct entity.
Many-to-many relationships use explicit associative entities.
Versioned concepts are represented explicitly.
Quantity and money have units.
Effective dates are supported where necessary.
