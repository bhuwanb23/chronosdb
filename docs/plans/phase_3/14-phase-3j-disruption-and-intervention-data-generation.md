14. Phase 3J: Disruption and Intervention Data Generation
Goal

Generate scenario inputs that exercise ChronosDB’s decision logic.

Supported benchmark event categories

Although the winning MVP focuses on supplier outage, controlled benchmark coverage may include:

Plain Text
SUPPLIER_OUTAGE
SHIPMENT_DELAY
DEMAND_SPIKE
INVENTORY_LOSS
FACILITY_CAPACITY_REDUCTION

Only SUPPLIER_OUTAGE is mandatory for the initial application path. Other categories can remain future benchmark fixtures if Phase 1 deferred their implementation.

Supplier-outage parameters

Generate variations in:

Supplier
Scope
Start time
Duration
Affected purchase orders
Recovery lag
Inventory coverage
Alternate-supplier availability
Customer-order priority
Budget
Intervention parameter records

Generate:

Transfer lanes
Transfer costs
Transfer lead times
Expedition eligibility
Expedition cost
Alternate supplier capacity
Alternate supplier lead time
Alternate supplier premium
Rescheduling rules
Production capacity
Scenario difficulty levels
Level 1: Direct
One supplier
One component
One product
One order
One obvious intervention
Level 2: Connected
One supplier
Multiple components or products
Several customer orders
Multiple interventions
Level 3: Constrained
Budget conflict
Safety-stock limit
Supplier capacity
Customer priorities
No universally best intervention
Level 4: Adversarial
Missing data
Contradictory data
No feasible intervention
Tied candidates
Late correction
Unsupported event combination
Deliverables
Plain Text
data/generated/scenarios/
├── disruptions.csv
├── scenario_definitions.json
├── scenario_constraints.json
├── candidate_parameters.json
└── intervention_costs.csv
