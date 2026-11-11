Phase 2 Deep Dive: Domain, Temporal and Causal Model

I will preserve this format for every subsequent ChronosDB phase automatically: objectives, boundaries, subphases, technical decisions, artifacts, benchmarks, acceptance tests, risks, execution order, exit gate, and next-phase handoff.

Phase 0 established the project foundation. Phase 1 locked the product contract. Phase 2 now defines the formal supply-chain world that ChronosDB will reason over.

This is a critical architecture phase. If the domain rules are vague, the dataset will be inconsistent, the simulation will be misleading, and benchmark results will have no defensible ground truth.

1. Phase Definition
Phase name

Domain, Temporal and Causal Model

Primary goal

Create a precise, internally consistent and testable model of:

Suppliers
Components
Products and bills of material
Warehouses and inventory
Purchase orders
Production orders
Customer orders
Disruptions
Interventions
Time
Dependencies
Constraints
Costs
Service-level impact
Counterfactual outcomes
Required result

At the end of Phase 2, ChronosDB must have a specification capable of answering, without ambiguity:

What constitutes the operational state of the supply chain?
Which records are facts, events, plans or derived states?
How does a supplier outage propagate through the system?
How is inventory availability calculated?
When does a component shortage occur?
When does a production order become delayed?
When does a customer order breach its SLA?
How is revenue at risk calculated?
Which interventions are feasible?
How do interventions change the baseline state?
How is historical state reconstructed?
How are counterfactual futures isolated?
Which formulas produce every important metric?
Which results are exact, assumed or uncertain?
What is the manually verified golden scenario?
2. Phase 2 Definition of Done

Phase 2 is complete only when this statement is true:

Given a supplier outage and a defined operational state, an independent engineer can manually determine the affected components, inventory shortages, production delays, customer-order impact, SLA breaches, revenue at risk, feasible interventions and expected best recovery plan using the Phase 2 rules alone.

No implementation-specific database schema is required yet, but the model must be precise enough that Phase 3 can generate valid data and Phase 4 can design the Db2 schema without inventing business behavior.

3. Phase 2 Boundaries
In scope
Domain entities
Entity relationships
Entity lifecycle and state
Units and quantities
Time semantics
Operational events
Supplier-outage propagation
Inventory allocation rules
BOM dependencies
Production scheduling assumptions
Customer-order commitments
Intervention feasibility
Cost calculations
Revenue-at-risk definition
Causal graph
Counterfactual model
Golden scenario
Domain invariants
Formula catalogue
Manual validation
Domain benchmark specification
Out of scope
Physical Db2 table design
SQL migrations
Final indexes
Synthetic-data generation code
Production simulation code
Optimization algorithm implementation
Vector embedding design
LangChain prompts
API design
UI design
Performance optimization
Monte Carlo forecasting
Live ERP integration
Autonomous execution

These belong to later phases.

4. Phase 2 Structure
Plain Text
Phase 2
├── 2A. Phase 1 handoff validation
├── 2B. Domain language and bounded context
├── 2C. Entity and value-object model
├── 2D. Relationship and dependency model
├── 2E. State and lifecycle model
├── 2F. Unit, quantity and financial model
├── 2G. Temporal model
├── 2H. Event and disruption model
├── 2I. Inventory availability and allocation model
├── 2J. BOM and material-requirement model
├── 2K. Production scheduling model
├── 2L. Customer-order and SLA model
├── 2M. Causal propagation model
├── 2N. Intervention model
├── 2O. Counterfactual scenario model
├── 2P. Cost, impact and objective formulas
├── 2Q. Evidence and provenance model
├── 2R. Uncertainty and data-quality model
├── 2S. Golden scenario construction
├── 2T. Domain test and benchmark specification
├── 2U. Domain review and falsification
└── 2V. Phase 3 handoff
5. Phase 2A: Phase 1 Handoff Validation
Goal

Confirm that the domain model is built from the locked product specification rather than assumptions introduced during modelling.

Required Phase 1 inputs

Verify:

Product identity
Primary persona
Stakeholder map
Decision specification
End-to-end journey
Use-case catalogue
Functional requirements
Non-functional requirements
Data requirements
Evidence requirements
AI authority contract
Scope register
Measurement contract
Product acceptance tests
Phase 2 question register
Requirements traceability matrix
Handoff invariants

The following remain locked:

Plain Text
Primary scenario:
Supplier outage
 
Primary decision:
Which feasible intervention minimizes operational impact
under explicit constraints?
 
Primary calculation authority:
Deterministic Python and SQL
 
Primary system of record:
IBM Db2
 
Primary outputs:
Shortages, delays, SLA breaches, revenue at risk,
intervention cost, recommendation and evidence
 
Human role:
Review and approve recommendations
Deliverable
Plain Text
docs/domain/phase-1-handoff-review.md
Exit gate
Every required product input exists.
No Phase 2 rule contradicts Phase 1.
Unresolved product questions are listed.
The MVP remains limited to the supplier-outage vertical slice.
No new feature is introduced without scope review.
6. Phase 2B: Domain Language and Bounded Context
Goal

Create a controlled vocabulary so every term has one meaning.

6.1 Bounded context

The MVP models a simplified manufacturing supply-chain planning context.

It includes:

Plain Text
Supplier procurement
→ Inbound replenishment
→ Warehouse inventory
→ Material allocation
→ Production fulfilment
→ Customer-order delivery

It does not attempt to model:

Full accounting
Detailed transportation routing
Customs clearance
Supplier-contract negotiation
Machine-level production
Workforce scheduling
Product returns
Invoice settlement
6.2 Ubiquitous language
Supplier

An organization approved to provide one or more components.

Component

A purchased or stocked material consumed to produce a finished product.

Product

A finished good associated with a bill of materials.

Bill of materials

A versioned definition of the components and quantities required to produce one unit of a product.

Warehouse

A location holding component inventory.

Facility

A location executing production orders.

Inventory lot

A time- and location-specific quantity of a component.

On-hand inventory

Physical quantity recorded at a warehouse.

Reserved inventory

Quantity committed to demand and unavailable to unrelated demand.

Available inventory

Quantity that may be allocated after reservations and applicable controls.

Safety stock

Minimum inventory that should remain after an optional transfer or allocation.

Purchase order

A planned inbound quantity from a supplier.

Production order

An instruction to produce a quantity of a finished product at a facility.

Customer order

A customer commitment for a product quantity and promised delivery date.

Supplier outage

A time-bounded event that prevents or delays specified supply from a supplier.

Scenario

An immutable definition of an operational state, disruption, objective and constraints.

Intervention

A proposed change intended to reduce disruption impact.

Simulation run

A deterministic evaluation of one scenario and one intervention.

Baseline

The projected operational outcome without the new disruption.

Do-nothing case

The projected operational outcome with the disruption but without a recovery intervention.

These two terms must not be confused.

Revenue at risk

The allocated order-line revenue associated with projected late or unfulfilled quantity.

It is not confirmed revenue loss.

SLA breach

A projected delivery condition that violates the applicable customer-service commitment.

Feasible intervention

An intervention satisfying every applicable hard constraint.

Recommendation

The highest-ranked feasible intervention under the chosen objective.

Deliverables
Plain Text
docs/domain/domain-glossary.md
docs/domain/bounded-context.md
Terminology gate
Every major term has exactly one definition.
Baseline and do-nothing are distinct.
Revenue at risk and revenue lost are distinct.
Facts and projections are distinguishable.
Scenario and intervention are distinct.
Warehouse and production facility are distinct.
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
8. Phase 2D: Relationship and Dependency Model
Goal

Define cardinalities and dependency paths.

Core relationships
Plain Text
Supplier 1 ──< SupplierComponent >── 1 Component
 
Product 1 ──< BOMVersion 1 ──< BOMLine >── 1 Component
 
Warehouse 1 ──< InventorySnapshot >── 1 Component
 
Supplier 1 ──< PurchaseOrder >── 1 Component
 
Facility 1 ──< ProductionOrder >── 1 Product
 
ProductionOrder 1 ──< ProductionMaterialAllocation >── Component
 
CustomerOrder 1 ──< CustomerOrderLine >── Product
 
CustomerOrderLine 0..1 ── ProductionOrder
 
Scenario 1 ──< Intervention
 
Scenario 1 ──< SimulationRun
Intervention 1 ──< SimulationRun
Important cardinality decisions
Supplier and component
One supplier may supply many components.
One component may have many approved suppliers.
Approval is time-dependent.
Product and component
One product contains many BOM lines.
One component may appear in many products.
BOM version is selected based on operational time.
Production and customer orders

For MVP simplicity:

Each customer-order line may be associated with one production order.
One production order may fulfil multiple customer-order lines.
Partial fulfilment may occur.
Warehouse and facility

A production facility may consume from:

One default warehouse
Additional eligible warehouses through transfers

The default source and transfer eligibility must be explicit.

Dependency graph

The primary causal dependency is:

Plain Text
Supplier
→ Purchase order or expected replenishment
→ Component available quantity
→ Material allocation
→ Production order start/completion
→ Customer-order fulfilment
→ Delivery projection
→ SLA status
→ Revenue at risk
Deliverables
Plain Text
docs/domain/relationship-model.md
docs/domain/dependency-graph.md
Exit gate
Every causal edge corresponds to a documented relationship.
No hidden relationship is required for the golden scenario.
Cardinalities support alternate suppliers and multi-component products.
Customer impact can be traced back to supplier supply.
The graph is acyclic for the MVP calculation path.
9. Phase 2E: State and Lifecycle Model
Goal

Define valid status values and state transitions.

9.1 Scenario lifecycle
Plain Text
DRAFT
→ VALIDATED
→ FROZEN
→ SIMULATING
→ COMPLETED

Failure transitions:

Plain Text
DRAFT → REJECTED
VALIDATED → REJECTED
SIMULATING → PARTIALLY_COMPLETED
SIMULATING → FAILED

Rules:

Only a validated scenario may be frozen.
Frozen scenario inputs are immutable.
Re-running creates a new simulation run.
Failure must not modify original input.
9.2 Purchase-order lifecycle
Plain Text
DRAFT
→ CONFIRMED
→ IN_TRANSIT
→ PARTIALLY_RECEIVED
→ RECEIVED

Alternative states:

Plain Text
CANCELLED
DELAYED

Only outstanding quantity is affected by an outage.

Qoutstanding=max⁡(0,Qordered−Qreceived)Q_{outstanding} = \max(0, Q_{ordered} - Q_{received})Qoutstanding​=max(0,Qordered​−Qreceived​)
9.3 Production-order lifecycle
Plain Text
PLANNED
→ RELEASED
→ IN_PROGRESS
→ COMPLETED

Alternative states:

Plain Text
BLOCKED
DELAYED
CANCELLED
MVP disruption treatment
Completed quantity is not undone.
Only the uncompleted portion is evaluated.
An in-progress order may already have consumed allocated materials.
Planned orders compete for future material.
9.4 Customer-order lifecycle
Plain Text
OPEN
→ ALLOCATED
→ IN_PRODUCTION
→ READY
→ SHIPPED
→ DELIVERED

Alternative states:

Plain Text
DELAYED
CANCELLED
9.5 Intervention lifecycle
Plain Text
GENERATED
→ VALIDATING
→ FEASIBLE
→ SIMULATED
→ RANKED
→ RECOMMENDED

Alternative states:

Plain Text
INFEASIBLE
INSUFFICIENT_DATA
SIMULATION_FAILED
Deliverable
Plain Text
docs/domain/state-transition-model.md
Exit gate
Every state has an entry condition.
Every transition has a valid trigger.
Terminal and recoverable failures are separated.
Completed operational work cannot be reversed by simulation.
Insufficient data is not treated as infeasibility.
10. Phase 2F: Unit, Quantity and Financial Model
Goal

Prevent silent unit errors and misleading financial calculations.

10.1 Unit-of-measure policy

Each component has one canonical inventory unit.

Examples:

Plain Text
EA = each
KG = kilogram
L = litre
M = metre

MVP recommendation:

Use EA for all golden-scenario electronic components.
Do not introduce conversion unless required.
Reject incompatible units.
10.2 Quantity precision

Recommended conceptual precision:

Plain Text
Component quantity: decimal, not floating point
Product quantity: integer for discrete finished goods
Money: fixed decimal
Percentages: decimal from 0 to 1
10.3 Currency policy

Use one canonical MVP currency:

Plain Text
INR

All costs and revenue values in the golden dataset use INR.

Multi-currency conversion is deferred.

10.4 Rounding policy
Preserve full internal decimal precision.
Round money only for presentation.
Use two decimal places for INR calculations.
Do not round intermediate quantities unless the component requires integer units.
Round projected timestamps only if the scheduling model defines it.
10.5 Financial distinctions
Order-line revenue
Rline=Qordered×PunitR_{line} = Q_{ordered} \times P_{unit}Rline​=Qordered​×Punit​
Late quantity revenue at risk
RARline=Qlate×PunitRAR_{line} = Q_{late} \times P_{unit}RARline​=Qlate​×Punit​

Do not automatically classify the entire order-line revenue as at risk when only part of the quantity is late.

Intervention cost

May include:

Alternate supplier price premium
Expedite fee
Transfer transportation cost
Rescheduling penalty
Overtime cost, if modelled

MVP recommendation:

Cintervention=Cpurchase premium+Cexpedite+Ctransfer+CrescheduleC_{intervention} = C_{purchase\ premium} + C_{expedite} + C_{transfer} + C_{reschedule}Cintervention​=Cpurchase premium​+Cexpedite​+Ctransfer​+Creschedule​
Deliverable
Plain Text
docs/domain/units-and-financial-model.md
Exit gate
Every quantity has a unit.
Every monetary value has a currency.
Revenue at risk supports partial quantity.
Costs are not double-counted.
Rounding rules are explicit.
11. Phase 2G: Temporal Model
Goal

Define exactly which time each record represents and how historical state is reconstructed.

11.1 Time dimensions
Event time

When something happened in the business world.

Example:

Plain Text
Supplier outage begins at 2026-11-11 08:00 IST
Reported time

When ChronosDB learned about an event.

Example:

Plain Text
Outage reported at 2026-11-11 09:15 IST
Ingestion time

When the record entered Db2.

Effective time

When a business record is considered valid.

Scenario as-of time

The point at which operational state is frozen for simulation.

Simulation horizon

The future interval over which impact is calculated.

11.2 Clock standard

Store canonical timestamps in UTC.

Display local time using:

Plain Text
Asia/Kolkata

The time zone must be attached to user-facing dates or documented globally.

11.3 Effective interval

Use:

[effective_from,effective_to)[effective\_from, effective\_to)[effective_from,effective_to)

A record is active at time ttt when:

effective_from≤t<effective_toeffective\_from \le t < effective\_toeffective_from≤t<effective_to

If effective_to is absent, the interval remains open.

11.4 Scenario state rule

The scenario uses records known and valid at its as_of_time.

Conceptually:

State(t)={r∣r.valid_at(t)∧r.known_by(t)}State(t) = \{r \mid r.valid\_at(t) \land r.known\_by(t)\}State(t)={r∣r.valid_at(t)∧r.known_by(t)}

For the MVP, avoid retroactive data corrections unless explicitly modelled.

11.5 Planning granularity

Use one-hour granularity for operational timestamps.

Business lead times may be expressed in days but converted to hours:

LeadTimeHours=LeadTimeDays×24LeadTimeHours = LeadTimeDays \times 24LeadTimeHours=LeadTimeDays×24

If working-day calendars are not implemented, explicitly state that lead times use elapsed calendar time.

11.6 Simulation horizon

Recommended golden scenario:

Plain Text
30 calendar days

The horizon must exceed the outage duration and expected recovery period.

11.7 Late-arriving data

If a record is ingested after scenario freeze:

It must not silently change the completed scenario.
A new scenario or state version is required.
Replay must preserve the original information state.
Deliverables
Plain Text
docs/domain/temporal-model.md
docs/domain/time-examples.md
Temporal acceptance tests
A BOM version ending at 10:00 is not active at 10:00.
The next BOM version beginning at 10:00 is active at 10:00.
A late-ingested disruption does not modify an earlier completed scenario.
An order received before the outage is not treated as outstanding supply.
A replenishment arriving after a shortage can resolve later demand but not earlier missed demand.
12. Phase 2H: Event and Disruption Model
Goal

Define how a supplier outage changes expected supply.

12.1 MVP event type
Plain Text
SUPPLIER_OUTAGE
Required parameters
Plain Text
supplier_id
start_time
end_time or duration
scope
severity
reported_time
Scope options
Plain Text
ALL_SUPPLY
SELECTED_COMPONENTS
SELECTED_PURCHASE_ORDERS

MVP golden scenario:

Plain Text
ALL_SUPPLY
12.2 Outage effect

For an affected purchase order with expected arrival during the outage:

Simple MVP rule

The affected outstanding quantity is delayed until:

Arrivalnew=max⁡(Arrivaloriginal,OutageEnd+RecoveryLag)Arrival_{new} = \max(Arrival_{original}, OutageEnd + RecoveryLag)Arrivalnew​=max(Arrivaloriginal​,OutageEnd+RecoveryLag)

Where:

Plain Text
RecoveryLag = supplier restart and logistics delay

Recommended initial recovery lag:

Plain Text
2 calendar days

This must be configurable.

12.3 Effect boundaries

An outage does not affect:

Quantity already received
Unaffected suppliers
Components outside disruption scope
Purchase orders arriving before outage start
Cancelled purchase orders
Purchase orders after outage if supplier capacity permits
12.4 Post-outage capacity

MVP simplification:

Supply resumes at normal capacity after recovery lag.
No backlog-capacity competition is initially modelled.

This assumption must be recorded because real suppliers may require time to clear accumulated backlog.

12.5 Event precedence

If multiple events affect the same supply:

Phase 2 records the conceptual precedence rule.
Multi-event simulation remains deferred.
MVP rejects overlapping unmodelled disruptions rather than guessing.
Deliverable
Plain Text
docs/domain/disruption-model.md
Exit gate
Outage start and end semantics are precise.
Affected supply is deterministically identifiable.
Already received supply is protected.
Recovery lag is explicit.
Unsupported overlapping disruptions are rejected.
13. Phase 2I: Inventory Availability and Allocation Model
Goal

Define how material availability is calculated over time.

13.1 Inventory position

At warehouse www, component ccc, and time ttt:

AvailableInventoryw,c,t=OnHandw,c,t−Reservedw,c,t−Quarantinedw,c,tAvailableInventory_{w,c,t} = OnHand_{w,c,t} - Reserved_{w,c,t} - Quarantined_{w,c,t}AvailableInventoryw,c,t​=OnHandw,c,t​−Reservedw,c,t​−Quarantinedw,c,t​

For normal production use:

UsableInventory=max⁡(0,AvailableInventory)UsableInventory = \max(0, AvailableInventory)UsableInventory=max(0,AvailableInventory)
13.2 Projected inventory balance

For ordered event times t1…tnt_1 \dots t_nt1​…tn​:

Balancet=Balancet−1+Receiptst+TransfersInt−ProductionConsumptiont−TransfersOuttBalance_t = Balance_{t-1} + Receipts_t + TransfersIn_t - ProductionConsumption_t - TransfersOut_tBalancet​=Balancet−1​+Receiptst​+TransfersInt​−ProductionConsumptiont​−TransfersOutt​
13.3 Safety-stock distinction

Safety stock is not automatically unavailable for production in the MVP.

Recommended rule:

Production may consume below safety stock if required.
Optional warehouse transfers may not reduce the source warehouse below safety stock.
The resulting safety-stock breach is recorded as operational risk.

This prevents the model from declaring production impossible merely because inventory falls below a planning threshold.

13.4 Allocation priority

Recommended allocation sequence:

Already in-progress production orders
Released production orders
Higher-priority customer commitments
Earlier promised delivery
Earlier production-order creation
Stable identifier as deterministic tie-breaker
13.5 Reservation treatment

Avoid subtracting reservations twice.

Choose one authoritative approach.

Recommended model
Inventory snapshot stores physical on-hand and current reserved quantity.
Future simulation recalculates allocation from eligible demand.
The golden scenario explicitly identifies existing committed reservations.
13.6 Shortage definition

A shortage occurs when a material requirement cannot be fully allocated by the required consumption time.

ShortageQuantity=max⁡(0,RequiredQuantity−AllocatableQuantity)ShortageQuantity = \max(0, RequiredQuantity - AllocatableQuantity)ShortageQuantity=max(0,RequiredQuantity−AllocatableQuantity)
Shortage date

The earliest requirement time at which:

ProjectedBalancet<RequiredQuantitytProjectedBalance_t < RequiredQuantity_tProjectedBalancet​<RequiredQuantityt​
13.7 Warehouse-transfer availability

For a source warehouse:

TransferableQuantity=max⁡(0,ProjectedBalanceBeforeTransfer−SafetyStock−CommittedFutureDemand)TransferableQuantity = \max( 0, ProjectedBalanceBeforeTransfer - SafetyStock - CommittedFutureDemand )TransferableQuantity=max(0,ProjectedBalanceBeforeTransfer−SafetyStock−CommittedFutureDemand)

The planning window for committed demand must equal the scenario horizon or a defined transfer-protection window.

Deliverables
Plain Text
docs/domain/inventory-model.md
docs/domain/allocation-policy.md
Inventory invariants
Physical on-hand is never negative.
Allocated quantity never exceeds available eligible quantity.
Transfer quantity never exceeds transferable quantity.
The same inventory unit cannot be allocated to two production orders.
Reserved inventory is not subtracted twice.
Receipts cannot be consumed before arrival.
14. Phase 2J: BOM and Material-Requirement Model
Goal

Translate production quantity into component demand.

14.1 BOM selection

For production order ppp, select the BOM active at:

Plain Text
planned production start time

If no active BOM exists:

Plain Text
INSUFFICIENT_DATA

Do not silently select the latest BOM.

14.2 Component requirement

For product quantity QpQ_pQp​:

GrossRequirementp,c=Qp×BOMQuantityp,c×(1+ScrapFactorp,c)GrossRequirement_{p,c} = Q_p \times BOMQuantity_{p,c} \times (1 + ScrapFactor_{p,c})GrossRequirementp,c​=Qp​×BOMQuantityp,c​×(1+ScrapFactorp,c​)

For discrete components, round upward:

RequiredQuantityp,c=⌈GrossRequirementp,c⌉RequiredQuantity_{p,c} = \lceil GrossRequirement_{p,c} \rceilRequiredQuantityp,c​=⌈GrossRequirementp,c​⌉
14.3 Remaining production requirement

For partially completed production:

RemainingProductQuantity=PlannedQuantity−CompletedQuantityRemainingProductQuantity = PlannedQuantity - CompletedQuantityRemainingProductQuantity=PlannedQuantity−CompletedQuantity

Then calculate materials only for the remaining quantity unless material has already been issued.

14.4 Mandatory components

If a mandatory component is unavailable:

The affected production quantity cannot begin or complete.
Delay calculation continues until sufficient material becomes available.

Optional BOM components are out of MVP scope unless a substitution rule exists.

14.5 Substitution

Substitution is permitted only when:

Components share an approved substitution relationship.
Conversion ratio is defined.
Effective date is valid.
Product or BOM permits substitution.
Required qualification is valid.

For the MVP, alternate supplier is preferred over component substitution. Component substitution may be deferred unless needed for the golden scenario.

Deliverables
Plain Text
docs/domain/bom-model.md
docs/domain/material-requirement-formulas.md
Exit gate
The BOM version is time-valid.
Component requirement is reproducible.
Scrap factor is not double-counted.
Partial production is handled explicitly.
Missing BOM produces insufficient data, not zero demand.
15. Phase 2K: Production Scheduling Model
Goal

Define a deterministic but manageable production-delay model.

15.1 Scheduling assumptions

For the MVP:

A production order has a planned start and planned completion.
Required materials must be available before production starts.
Each facility has a daily finished-unit capacity.
Production orders are processed according to deterministic priority.
Preemption of in-progress production is not permitted.
Setup-time optimization is deferred.
15.2 Material-ready time
MaterialReadyTimep=max⁡c∈BOM(p)ComponentAvailableTimep,cMaterialReadyTime_p = \max_{c \in BOM(p)} ComponentAvailableTime_{p,c}MaterialReadyTimep​=c∈BOM(p)max​ComponentAvailableTimep,c​
15.3 Capacity-ready time

The earliest time the facility has sufficient production capacity.

This is based on:

Orders already in progress
Higher-priority orders
Facility daily capacity
Remaining production quantities
15.4 Projected start
ProjectedStartp=max⁡(PlannedStartp,MaterialReadyTimep,CapacityReadyTimep)ProjectedStart_p = \max( PlannedStart_p, MaterialReadyTime_p, CapacityReadyTime_p )ProjectedStartp​=max(PlannedStartp​,MaterialReadyTimep​,CapacityReadyTimep​)
15.5 Production duration
DurationDaysp=RemainingQuantitypFacilityDailyCapacityAllocatedpDurationDays_p = \frac{RemainingQuantity_p} {FacilityDailyCapacityAllocated_p}DurationDaysp​=FacilityDailyCapacityAllocatedp​RemainingQuantityp​​

For day-bucket MVP scheduling:

DurationDaysp=⌈RemainingQuantitypFacilityDailyCapacity⌉DurationDays_p = \left\lceil \frac{RemainingQuantity_p} {FacilityDailyCapacity} \right\rceilDurationDaysp​=⌈FacilityDailyCapacityRemainingQuantityp​​⌉
15.6 Projected completion
ProjectedCompletionp=ProjectedStartp+DurationpProjectedCompletion_p = ProjectedStart_p + Duration_pProjectedCompletionp​=ProjectedStartp​+Durationp​
15.7 Production delay
ProductionDelayHoursp=max⁡(0,ProjectedCompletionp−PlannedCompletionp)ProductionDelayHours_p = \max( 0, ProjectedCompletion_p - PlannedCompletion_p )ProductionDelayHoursp​=max(0,ProjectedCompletionp​−PlannedCompletionp​)

User-facing days may be:

ProductionDelayDaysp=ProductionDelayHoursp24ProductionDelayDays_p = \frac{ProductionDelayHours_p}{24}ProductionDelayDaysp​=24ProductionDelayHoursp​​

Do not mix rounded and unrounded values.

15.8 Priority

Recommended ordering:

In-progress order
Explicit production-order priority
Earliest associated customer promised date
Planned start
Production-order ID
Deliverables
Plain Text
docs/domain/production-scheduling-model.md
docs/domain/production-priority-policy.md
Exit gate
Material and capacity constraints are both considered.
The schedule is deterministic.
Ties have a stable resolution.
Existing completed output is preserved.
The model explicitly documents day-bucket simplification.
16. Phase 2L: Customer-Order and SLA Model
Goal

Translate production completion into customer impact.

16.1 Fulfilment model

For MVP:

A customer-order line is linked to a production order.
Completed product may fulfil one or more order lines.
Order lines are allocated by defined customer priority.
Shipping transit may use a fixed delivery lead time.

Recommended default:

Plain Text
Delivery lead time = 1 calendar day
16.2 Projected delivery
ProjectedDeliveryl=ProjectedProductAvailabilityl+DeliveryLeadTimelProjectedDelivery_l = ProjectedProductAvailability_l + DeliveryLeadTime_lProjectedDeliveryl​=ProjectedProductAvailabilityl​+DeliveryLeadTimel​
16.3 SLA classification

Recommended classifications:

Plain Text
ON_TIME
AT_RISK
BREACHED
INSUFFICIENT_DATA
During simulation
ON_TIME: projected delivery is on or before promised date.
BREACHED: projected delivery exceeds promised date.
AT_RISK: optional forward-looking warning when margin is below a configured threshold.
INSUFFICIENT_DATA: required date or fulfilment mapping is missing.

For benchmark simplicity, the core binary metric should use:

Plain Text
ON_TIME
BREACHED
16.4 Delay
CustomerDelayHoursl=max⁡(0,ProjectedDeliveryl−PromisedDeliveryl)CustomerDelayHours_l = \max( 0, ProjectedDelivery_l - PromisedDelivery_l )CustomerDelayHoursl​=max(0,ProjectedDeliveryl​−PromisedDeliveryl​)
16.5 Partial fulfilment

For an order line:

LateQuantityl=max⁡(0,OrderedQuantityl−OnTimeFulfilledQuantityl)LateQuantity_l = \max( 0, OrderedQuantity_l - OnTimeFulfilledQuantity_l )LateQuantityl​=max(0,OrderedQuantityl​−OnTimeFulfilledQuantityl​)
16.6 Revenue at risk
RevenueAtRiskl=LateQuantityl×UnitRevenuelRevenueAtRisk_l = LateQuantity_l \times UnitRevenue_lRevenueAtRiskl​=LateQuantityl​×UnitRevenuel​

Total:

TotalRevenueAtRisk=∑lRevenueAtRisklTotalRevenueAtRisk = \sum_l RevenueAtRisk_lTotalRevenueAtRisk=l∑​RevenueAtRiskl​
16.7 SLA breach count

Two separate measures are useful:

Breached order lines
Countlines=∣{l∣LateQuantityl>0}∣Count_{lines} = |\{l \mid LateQuantity_l > 0\}|Countlines​=∣{l∣LateQuantityl​>0}∣
Breached customer orders
Countorders=∣{o∣∃l∈o,LateQuantityl>0}∣Count_{orders} = |\{o \mid \exists l \in o, LateQuantity_l > 0\}|Countorders​=∣{o∣∃l∈o,LateQuantityl​>0}∣

The interface must label which one is shown.

Recommended headline metric:

Plain Text
Projected customer orders breached
Deliverables
Plain Text
docs/domain/customer-fulfilment-model.md
docs/domain/sla-and-revenue-model.md
Exit gate
Partial fulfilment is supported.
Promised date has a clear time zone and granularity.
Revenue at risk applies to late quantity.
Order-line and order-level breach counts are distinct.
Missing due dates produce insufficient data.
17. Phase 2M: Causal Propagation Model
Goal

Define the complete deterministic path from supplier disruption to business impact.

17.1 Causal graph
Plain Text
Supplier Outage
↓
Affected Outstanding Purchase Orders
↓
Delayed Component Receipts
↓
Lower Projected Component Balance
↓
Component Shortage
↓
Production Material Unavailability
↓
Delayed Production Start
↓
Delayed Production Completion
↓
Delayed Product Availability
↓
Delayed Customer Delivery
↓
SLA Breach
↓
Revenue at Risk
17.2 Causal edge contract

Every edge must define:

Source state
Transformation rule
Required data
Output state
Failure condition
Evidence trace

Example:

Plain Text
Edge:
Delayed receipt → component shortage
 
Required data:
Opening balance
Reserved quantity
Expected receipts
Production consumption
Receipt timestamps
 
Rule:
Ordered inventory balance calculation
 
Output:
Shortage date and quantity
 
Failure:
Missing opening inventory snapshot
17.3 Necessary versus contributing causes

ChronosDB should distinguish:

Necessary operational constraint

A missing mandatory component that directly blocks production.

Contributing factor

A low safety-stock level that makes disruption impact worse but does not independently cause the outage.

Contextual evidence

A historical incident that helps explain risk but does not establish current causality.

17.4 Causal trace

Every affected customer-order line should support a trace like:

Plain Text
Supplier S-104 outage
→ PO-2208 delayed
→ C-042 receipt delayed by 14 days
→ C-042 shortage of 320 units on 14 Nov
→ Production order PROD-876 starts 6 days late
→ Customer order CO-701 delivered 5 days late
→ ₹420,000 revenue at risk
17.5 No unsupported causal jumps

The system must not jump directly from:

Plain Text
Supplier outage → revenue loss

Instead it must preserve intermediate dependencies.

Deliverables
Plain Text
docs/domain/causal-model.md
docs/domain/causal-edge-catalogue.md
docs/domain/causal-trace-format.md
Causal completeness metric
CC=business impact outputs with complete causal pathsall business impact outputsCC = \frac{\text{business impact outputs with complete causal paths}} {\text{all business impact outputs}}CC=all business impact outputsbusiness impact outputs with complete causal paths​

Target for the golden scenario:

Plain Text
100%
18. Phase 2N: Intervention Model
Goal

Define how recovery actions alter the disrupted scenario.

18.1 Do nothing
State change

None.

Purpose

Provides the required disrupted baseline for all comparisons.

18.2 Warehouse inventory transfer
Inputs
Plain Text
source_warehouse
destination_warehouse
component
quantity
transfer_start
transfer_lead_time
transfer_cost
Hard constraints
Source inventory exists.
Transfer does not violate protected safety stock.
Quantity is positive.
Destination is eligible.
Arrival occurs within simulation horizon.
Material is not already allocated elsewhere.
State changes
Plain Text
Source projected balance decreases at dispatch.
Destination projected balance increases at arrival.
Transfer cost is added.
18.3 Expedite purchase order
Inputs
Plain Text
purchase_order
new_arrival_time
expedite_cost
Hard constraints
Purchase order is outstanding.
Purchase order is expedite-eligible.
New arrival precedes disrupted arrival.
Supplier outage does not make expedition physically impossible.
Cost is within budget.
State changes
Plain Text
Receipt timestamp changes.
Expedite cost is added.

Important: Expediting cannot magically override a total supplier outage unless the order had already left the supplier or the model explicitly supports another logistics path.

18.4 Alternate supplier
Inputs
Plain Text
alternate_supplier
component
quantity
order_time
lead_time
unit_price
Hard constraints
Supplier-component relationship is approved.
Agreement is effective.
Quantity satisfies minimum order.
Quantity does not exceed capacity.
Arrival falls within horizon.
Cost is within budget.
Cost
AlternateSupplyCost=Quantity×AlternateUnitPriceAlternateSupplyCost = Quantity \times AlternateUnitPriceAlternateSupplyCost=Quantity×AlternateUnitPrice

Incremental intervention cost should compare against normal expected procurement cost:

SupplierPremium=Quantity×(AlternateUnitPrice−BaselineUnitPrice)SupplierPremium = Quantity \times (AlternateUnitPrice - BaselineUnitPrice)SupplierPremium=Quantity×(AlternateUnitPrice−BaselineUnitPrice)

If the alternative replaces an existing purchase, avoid counting full purchase cost as purely incremental.

18.5 Production rescheduling
Inputs
Plain Text
affected_production_order
new_priority
new_sequence
reschedule_cost
Hard constraints
Order is not completed.
Locked in-progress work is not preempted.
Facility capacity remains valid.
Rescheduling does not create hidden infeasibility.
Any new customer impact is included.
State changes

Production priority and capacity allocation change.

The model must calculate both:

Orders helped
Orders harmed

18.6 Hybrid intervention

Recommended first hybrid:

Plain Text
Warehouse transfer
+
Alternate supplier

The combination must be simulated as one intervention, not by adding separate outcome metrics.

18.7 Feasibility status
Plain Text
FEASIBLE
INFEASIBLE
INSUFFICIENT_DATA
UNSUPPORTED
18.8 Rejection codes

Examples:

Plain Text
SOURCE_SAFETY_STOCK_VIOLATION
INSUFFICIENT_TRANSFERABLE_QUANTITY
SUPPLIER_NOT_APPROVED
SUPPLIER_CAPACITY_EXCEEDED
MINIMUM_ORDER_NOT_MET
RECOVERY_BUDGET_EXCEEDED
PO_NOT_EXPEDITE_ELIGIBLE
OUTAGE_PREVENTS_EXPEDITION
ARRIVAL_OUTSIDE_HORIZON
PRODUCTION_ORDER_LOCKED
MISSING_REQUIRED_DATA
Deliverable
Plain Text
docs/domain/intervention-model.md
docs/domain/feasibility-rule-catalogue.md
Exit gate
Every intervention has explicit parameters.
Every intervention has hard constraints.
Every intervention has deterministic state changes.
Infeasibility has a machine-readable reason.
An intervention cannot create material from nothing.
19. Phase 2O: Counterfactual Scenario Model
Goal

Define how alternative futures are generated without modifying operational truth.

19.1 Scenario composition

A scenario consists of:

Scenario=BaselineState+Disruption+Objective+Constraints+SimulationHorizon+RuleVersionScenario = BaselineState + Disruption + Objective + Constraints + SimulationHorizon + RuleVersionScenario=BaselineState+Disruption+Objective+Constraints+SimulationHorizon+RuleVersion

An intervention run consists of:

CounterfactualRun=Scenario+InterventionOverlayCounterfactualRun = Scenario + InterventionOverlayCounterfactualRun=Scenario+InterventionOverlay
19.2 State layers
Layer 1: Operational state

The factual state at the scenario as_of_time.

Layer 2: Disruption overlay

Changes expected future supply.

Layer 3: Intervention overlay

Changes future receipts, transfers, allocation or schedule.

Layer 4: Derived outcome

Calculated shortages, delays, SLA breaches and financial impact.

19.3 Immutability
Layer 1 is immutable during simulation.
Layer 2 is immutable for all candidates in one scenario.
Each Layer 3 intervention is isolated.
Layer 4 is stored per run.
19.4 Comparability

All candidates within a scenario must use:

Same baseline state
Same disruption
Same simulation horizon
Same business-rule version
Same objective definitions
Same cost basis

Otherwise comparisons are invalid.

19.5 Determinism

Given identical:

Plain Text
baseline_state_version
disruption
intervention
constraint_set
rule_version

the outcome must be identical.

19.6 Outcome delta

For candidate iii:

RevenueProtectedi=RevenueAtRiskDoNothing−RevenueAtRiskiRevenueProtected_i = RevenueAtRisk_{DoNothing} - RevenueAtRisk_iRevenueProtectedi​=RevenueAtRiskDoNothing​−RevenueAtRiski​ SLABreachesAvoidedi=SLABreachesDoNothing−SLABreachesiSLABreachesAvoided_i = SLABreaches_{DoNothing} - SLABreaches_iSLABreachesAvoidedi​=SLABreachesDoNothing​−SLABreachesi​ DelayReductioni=TotalDelayDoNothing−TotalDelayiDelayReduction_i = TotalDelay_{DoNothing} - TotalDelay_iDelayReductioni​=TotalDelayDoNothing​−TotalDelayi​
Deliverable
Plain Text
docs/domain/counterfactual-model.md
Exit gate
Operational facts cannot be modified by a scenario.
Candidates share the same comparison base.
Every output has a scenario and run identity.
Same inputs produce identical outputs.
Deltas always name their reference case.
20. Phase 2P: Cost, Impact and Objective Formulas
Goal

Freeze mathematical definitions before code and data generation.

20.1 Core impact metrics
Affected components

A component is affected when the disruption changes at least one expected receipt or causes a projected shortage relative to the no-disruption baseline.

Maintain both:

Plain Text
Supply-affected components
Shortage-affected components
Affected production order

A production order is affected when its projected start or completion changes because of the disruption.

Affected customer order

A customer order is affected when at least one line has a changed projected delivery date.

SLA breach

A customer order is projected to breach when at least one required order line is late under the defined fulfilment rule.

Total delay

Recommended customer-impact measure:

TotalDelayHours=∑lLateQuantityl×DelayHourslTotalDelayHours = \sum_l LateQuantity_l \times DelayHours_lTotalDelayHours=l∑​LateQuantityl​×DelayHoursl​

This is quantity-weighted delay.

Also report:

Plain Text
Maximum customer delay
Average breached-line delay
Breached-order count
20.2 Cost metrics
Transfer cost
TransferCost=FixedTransferCost+Quantity×VariableCostPerUnitTransferCost = FixedTransferCost + Quantity \times VariableCostPerUnitTransferCost=FixedTransferCost+Quantity×VariableCostPerUnit
Expedite cost
ExpediteCost=FixedExpediteFee+OutstandingQuantity×ExpediteCostPerUnitExpediteCost = FixedExpediteFee + OutstandingQuantity \times ExpediteCostPerUnitExpediteCost=FixedExpediteFee+OutstandingQuantity×ExpediteCostPerUnit
Alternate supplier premium
AlternatePremium=Quantity×max⁡(0,AlternateUnitPrice−BaselineUnitPrice)AlternatePremium = Quantity \times \max(0, AlternateUnitPrice - BaselineUnitPrice)AlternatePremium=Quantity×max(0,AlternateUnitPrice−BaselineUnitPrice)

If the alternate supplier is cheaper, record savings separately rather than allowing negative intervention cost to distort comparisons.

Rescheduling cost

MVP may use a fixed, documented cost per affected production-order change.

20.3 Revenue protected
RevenueProtectedi=max⁡(0,RevenueAtRiskDoNothing−RevenueAtRiski)RevenueProtected_i = \max( 0, RevenueAtRisk_{DoNothing} - RevenueAtRisk_i )RevenueProtectedi​=max(0,RevenueAtRiskDoNothing​−RevenueAtRiski​)
20.4 Net protected value

Optional explanatory metric:

NetProtectedValuei=RevenueProtectedi−InterventionCostiNetProtectedValue_i = RevenueProtected_i - InterventionCost_iNetProtectedValuei​=RevenueProtectedi​−InterventionCosti​

Do not treat this as profit because revenue at risk is not guaranteed loss.

20.5 Objective modes
Minimize SLA breaches

Lexicographic ranking:

Fewest breached customer orders
Lowest revenue at risk
Lowest intervention cost
Lowest total delay
Stable intervention ID
Minimize revenue at risk
Lowest revenue at risk
Fewest SLA breaches
Lowest cost
Lowest delay
Minimize recovery cost
Lowest intervention cost
Subject to service-level constraint
Lowest revenue at risk
Lowest delay
Balanced recovery

Use normalized metrics:

Scorei=wsSi+wrRi+wdDi+wcCiScore_i = w_s S_i + w_r R_i + w_d D_i + w_c C_iScorei​=ws​Si​+wr​Ri​+wd​Di​+wc​Ci​

Where each normalized value is in [0,1][0,1][0,1], and lower is better.

Suggested default weights:

Plain Text
SLA breach score: 0.40
Revenue-at-risk score: 0.30
Delay score: 0.20
Recovery-cost score: 0.10

Weights must sum to 1.

Normalization

For metric xxx:

Normalized(xi)=xi−min⁡(x)max⁡(x)−min⁡(x)Normalized(x_i) = \frac{x_i - \min(x)} {\max(x) - \min(x)}Normalized(xi​)=max(x)−min(x)xi​−min(x)​

If all candidates have equal values:

Normalized(xi)=0Normalized(x_i) = 0Normalized(xi​)=0
20.6 Hard constraints before ranking

A candidate violating a hard constraint is excluded from recommendation ranking.

Hard constraints include:

Approval
Capacity
Inventory
Budget
Safety stock
Time horizon
Valid state transition
Deliverables
Plain Text
docs/domain/formula-catalogue.md
docs/domain/objective-and-ranking-model.md
Formula gate

Every formula must identify:

Formula ID
Inputs
Units
Output
Preconditions
Rounding
Edge cases
Example
Owning requirement
Future implementation phase
21. Phase 2Q: Evidence and Provenance Model
Goal

Ensure every important result can be explained and audited later.

21.1 Evidence categories
Operational evidence
Supplier record
Purchase order
Inventory snapshot
BOM version
Production order
Customer order
Rule evidence
Formula ID
Allocation rule
Scheduling rule
Feasibility rule
Objective version
Contextual evidence
Disruption report
Recovery procedure
Historical incident
Execution evidence
Scenario ID
Simulation run ID
Input-state version
Rule version
Timestamp
System version
21.2 Provenance chain

For a displayed metric:

Plain Text
Displayed claim
→ Derived output field
→ Calculation step
→ Rule ID
→ Input records
→ State version
→ Scenario and simulation run
21.3 Example
Plain Text
Claim:
Customer order CO-701 will be five days late.
 
Derived value:
projected_delay_hours = 120
 
Rule:
SLA-003
 
Inputs:
CO-701 promised delivery
PROD-876 projected completion
delivery lead time
 
Causal source:
C-042 shortage caused by delayed PO-2208
 
Run:
SIM-GOLD-DO-NOTHING
21.4 Provenance completeness

A result is not presentation-ready unless:

Its source records are identified.
Its formula version is identified.
Its scenario run is identified.
Its unit is specified.
Its reference case is specified if it is a delta.
Deliverable
Plain Text
docs/domain/provenance-model.md
Benchmark
ProvenanceCoverage=key outputs with complete provenanceall key outputsProvenanceCoverage = \frac{\text{key outputs with complete provenance}} {\text{all key outputs}}ProvenanceCoverage=all key outputskey outputs with complete provenance​

Golden scenario target:

Plain Text
100%
22. Phase 2R: Uncertainty and Data-Quality Model
Goal

Prevent incomplete or assumed data from appearing as precise truth.

22.1 Information classes
OBSERVED

Directly stored operational fact.

DERIVED

Calculated deterministically from observed facts.

ASSUMED

Configured simplification.

Examples:

One-day delivery lead time
Two-day supplier recovery lag
PROJECTED

Future outcome produced by deterministic simulation.

GENERATED

Natural-language explanation produced by AI.

22.2 Data completeness state

For each scenario:

Plain Text
COMPLETE
PARTIAL_NONCRITICAL
PARTIAL_CRITICAL
INVALID
Critical missing data

Examples:

No active BOM
No inventory state
Missing promised delivery
Missing production-order mapping
Unknown supplier relationship

Critical missing data must block the affected calculation.

22.3 No implicit zero rule

Missing values are never automatically treated as:

Plain Text
0 inventory
0 cost
0 lead time
0 revenue
0 demand

Use:

Plain Text
UNKNOWN
NOT_APPLICABLE
ZERO

as distinct concepts.

22.4 Confidence classification

Do not invent a percentage confidence score.

Recommended qualitative classification:

Plain Text
HIGH_EVIDENCE
MEDIUM_EVIDENCE
LOW_EVIDENCE
INSUFFICIENT_EVIDENCE

Example criteria:

High evidence
All critical structured records exist.
No major assumption drives the recommendation.
Causal trace is complete.
Medium evidence
Critical records exist.
One or more configured assumptions affect timing or cost.
Low evidence
Noncritical data is missing.
The recommendation is sensitive to an assumption.
Insufficient evidence
A critical calculation cannot be completed.
Deliverable
Plain Text
docs/domain/uncertainty-and-data-quality-model.md
Exit gate
Missing and zero are distinct.
Facts and assumptions are labelled.
Confidence does not use arbitrary percentages.
Critical missing data blocks affected calculations.
Partial results remain visible when safe.
23. Phase 2S: Golden Scenario Construction
Goal

Create one fully worked example that validates the entire model.

This scenario becomes the foundation for:

Phase 3 dataset generation
Phase 4 schema validation
Phase 5 impact-engine testing
Phase 6 simulation testing
Phase 7 optimization testing
The demo
Benchmark ground truth
23.1 Golden scenario setting
Organization

A synthetic electronics manufacturer.

Facilities
Plain Text
FAC-PUNE

Capacity:

Plain Text
100 finished units per day
Warehouses
Plain Text
WH-PUNE
WH-CHENNAI
Critical component
Plain Text
C-MCU-42

Unit:

Plain Text
EA
Finished product
Plain Text
P-CONTROLLER-X
BOM

Each controller requires:

Plain Text
2 × C-MCU-42

No scrap factor for the golden case.

23.2 Suppliers
Primary supplier
Plain Text
Supplier: S-104
Component: C-MCU-42
Normal lead time: 7 days
Unit price: ₹1,000
Approval: APPROVED
Alternate supplier
Plain Text
Supplier: S-208
Component: C-MCU-42
Lead time: 5 days
Unit price: ₹1,180
Daily capacity: 100 units
Minimum order: 100 units
Approval: APPROVED
23.3 Operational state

Scenario as-of time:

Plain Text
11 Nov 2026, 08:00 IST
Pune inventory
Plain Text
On hand: 400 MCU units
Reserved: 0
Safety stock: 100
Chennai inventory
Plain Text
On hand: 500 MCU units
Committed local demand: 180
Safety stock: 120

Transferable quantity:

500−180−120=200500 - 180 - 120 = 200500−180−120=200

Therefore:

Plain Text
Maximum transferable quantity = 200 MCU units

Transfer lead time:

Plain Text
2 days

Transfer cost:

Plain Text
₹40,000 fixed + ₹50 per unit

For 200 units:

₹40,000+(200×₹50)=₹50,000₹40,000 + (200 \times ₹50) = ₹50,000₹40,000+(200×₹50)=₹50,000
23.4 Purchase order
Plain Text
PO-2208
Supplier: S-104
Component: C-MCU-42
Outstanding quantity: 800 units
Original expected arrival: 13 Nov 2026
Destination: WH-PUNE
23.5 Disruption
Plain Text
Supplier S-104 outage
Start: 11 Nov 2026, 08:00 IST
Duration: 14 days
End: 25 Nov 2026, 08:00 IST
Recovery lag: 2 days

New arrival:

Plain Text
27 Nov 2026
23.6 Production orders
PROD-876
Plain Text
Product: P-CONTROLLER-X
Quantity: 200 units
MCU requirement: 400 units
Planned start: 12 Nov
Planned completion: 14 Nov
Customer line: CO-701-L1
PROD-882
Plain Text
Product: P-CONTROLLER-X
Quantity: 200 units
MCU requirement: 400 units
Planned start: 15 Nov
Planned completion: 17 Nov
Customer line: CO-704-L1
PROD-889
Plain Text
Product: P-CONTROLLER-X
Quantity: 200 units
MCU requirement: 400 units
Planned start: 18 Nov
Planned completion: 20 Nov
Customer line: CO-711-L1

Total MCU requirement:

400+400+400=1,200400 + 400 + 400 = 1,200400+400+400=1,200
23.7 Customer orders
CO-701
Plain Text
Quantity: 200 products
Promised delivery: 15 Nov
Unit revenue: ₹4,000
Order-line revenue: ₹800,000
Priority: HIGH
CO-704
Plain Text
Quantity: 200 products
Promised delivery: 18 Nov
Unit revenue: ₹4,000
Order-line revenue: ₹800,000
Priority: MEDIUM
CO-711
Plain Text
Quantity: 200 products
Promised delivery: 21 Nov
Unit revenue: ₹4,000
Order-line revenue: ₹800,000
Priority: MEDIUM

Total revenue:

₹2,400,000₹2,400,000₹2,400,000
23.8 Do-nothing calculation

Pune starts with:

Plain Text
400 MCU units

PROD-876 consumes:

Plain Text
400 MCU units

Remaining:

Plain Text
0

PO-2208 is delayed until 27 Nov.

Therefore:

PROD-876 remains on schedule.
PROD-882 cannot start until 27 Nov.
PROD-889 must follow capacity scheduling after PROD-882.

With one-day delivery lead time and 100-unit/day production capacity:

PROD-876
Plain Text
Start: 12 Nov
Complete: 14 Nov
Deliver: 15 Nov
CO-701: on time
PROD-882
Plain Text
Start: 27 Nov
Duration: 2 days
Complete: 29 Nov
Deliver: 30 Nov
CO-704 due: 18 Nov
Delay: 12 days
PROD-889
Plain Text
Start: 29 Nov
Duration: 2 days
Complete: 1 Dec
Deliver: 2 Dec
CO-711 due: 21 Nov
Delay: 11 days

Do-nothing result:

Plain Text
Breached orders: 2
Revenue at risk: ₹1,600,000
Quantity-weighted delay:
(200 × 12) + (200 × 11) = 4,600 unit-days
23.9 Candidate A: Transfer 200 MCU units

Arrival at Pune:

Plain Text
13 Nov

This supports:

Plain Text
100 finished products

But a production order requires 400 MCU units for 200 units if partial production is not enabled.

Phase 2 decision

We must explicitly choose whether partial production is allowed.

Recommended MVP decision:

Plain Text
Partial production is allowed in capacity-sized batches.

With 100-product batch:

Transfer supports half of PROD-882.
Production can complete 100 products.
The remaining quantity waits for later supply.
Partial customer delivery can reduce late quantity if allowed.

However, partial delivery adds significant complexity.

Recommended golden-scenario simplification

Increase transferable quantity to:

Plain Text
400 MCU units

To achieve this consistently, revise Chennai inventory:

Plain Text
On hand: 700
Committed demand: 180
Safety stock: 120
Transferable: 400

Use this corrected value for the locked golden scenario.

Transfer cost:

₹40,000+(400×₹50)=₹60,000₹40,000 + (400 \times ₹50) = ₹60,000₹40,000+(400×₹50)=₹60,000

This fully rescues PROD-882.

23.10 Candidate B: Alternate supplier

Order:

Plain Text
400 MCU units

Lead time:

Plain Text
5 days

Arrival:

Plain Text
16 Nov

Supplier premium:

400×(₹1,180−₹1,000)=₹72,000400 \times (₹1,180 - ₹1,000) = ₹72,000400×(₹1,180−₹1,000)=₹72,000

This can support one production order.

23.11 Candidate C: Hybrid intervention
Plain Text
Transfer 400 MCU units from Chennai
+
Order 400 MCU units from S-208

Arrivals:

Plain Text
Transfer: 13 Nov
Alternate supplier: 16 Nov

This provides enough material for PROD-882 and PROD-889 before disrupted PO arrival.

Cost:

₹60,000+₹72,000=₹132,000₹60,000 + ₹72,000 = ₹132,000₹60,000+₹72,000=₹132,000

Expected result:

Plain Text
CO-701: on time
CO-704: projected on time or near original plan
CO-711: projected on time or near original plan
Breached orders: 0
Revenue at risk: ₹0
Revenue protected: ₹1,600,000
Intervention cost: ₹132,000

The precise production sequence must be recalculated using the locked material arrival and facility-capacity rules.

23.12 Golden-scenario constraints
Plain Text
Maximum recovery budget: ₹200,000
Objective: Minimize SLA breaches
Approved suppliers only: Yes
Minimum source safety stock: Enforced
Simulation horizon: 30 days
Expected recommendation

Under the proposed values:

Plain Text
Hybrid intervention

Why:

Both affected customer orders can be protected.
The intervention remains under the ₹200,000 budget.
Approved supply is used.
Source safety stock remains protected.
It outperforms single interventions on SLA breaches.
Golden-scenario deliverables
Plain Text
docs/domain/golden-scenario/
├── scenario-definition.md
├── input-records.csv
├── manual-calculation.md
├── do-nothing-result.json
├── intervention-results.json
├── expected-recommendation.json
├── causal-traces.md
└── assumptions.md
Golden-scenario validation rule

At least two independent manual calculations should agree exactly on:

Shortage dates
Affected production orders
Completion dates
Customer delivery dates
SLA breaches
Revenue at risk
Intervention costs
Chosen recommendation
24. Phase 2T: Domain Test and Benchmark Specification
Goal

Create the model-level tests that later implementation must pass.

24.1 Entity tests
DT-ENT-001

A supplier-component relationship must reference an existing supplier and component.

DT-ENT-002

An inactive supplier cannot receive a new alternate order.

DT-ENT-003

A BOM line quantity must be positive.

DT-ENT-004

A customer order quantity must be positive.

24.2 Temporal tests
DT-TIME-001

Only the BOM version active at production time is used.

DT-TIME-002

A receipt cannot be consumed before its arrival.

DT-TIME-003

A completed scenario does not adopt late-ingested data.

DT-TIME-004

Overlapping active supplier agreements are rejected unless explicitly allowed.

24.3 Inventory tests
DT-INV-001

Allocated quantity cannot exceed eligible inventory.

DT-INV-002

A warehouse transfer cannot reduce source inventory below protected safety stock.

DT-INV-003

Quarantined inventory cannot be consumed.

DT-INV-004

Reserved inventory is not subtracted twice.

DT-INV-005

The same inventory cannot be allocated to multiple orders.

24.4 BOM tests
DT-BOM-001

Required quantity equals production quantity times BOM quantity.

DT-BOM-002

Scrap factor is applied exactly once.

DT-BOM-003

Missing active BOM returns insufficient data.

DT-BOM-004

Mandatory-component shortage blocks affected production.

24.5 Production tests
DT-PRD-001

Production cannot begin before materials are ready.

DT-PRD-002

Production cannot exceed facility capacity.

DT-PRD-003

Higher-priority orders are scheduled first.

DT-PRD-004

Tie-breaking is deterministic.

DT-PRD-005

Completed quantity is not rescheduled.

24.6 Customer-impact tests
DT-CUS-001

On-time delivery does not create revenue at risk.

DT-CUS-002

Partially late quantity creates proportional revenue at risk.

DT-CUS-003

Missing promised date yields insufficient data.

DT-CUS-004

Order-level breached count does not double-count multiple late lines.

24.7 Intervention tests
DT-INT-001

Unapproved alternate supplier is infeasible.

DT-INT-002

Budget-exceeding intervention is infeasible.

DT-INT-003

Expedition cannot bypass a total outage without supporting state.

DT-INT-004

Rescheduling includes negative impact on displaced orders.

DT-INT-005

Hybrid results are simulated jointly, not numerically added.

24.8 Causal tests
DT-CAU-001

Every breached customer line traces to at least one material or capacity constraint.

DT-CAU-002

An unaffected purchase order cannot appear in a disruption trace.

DT-CAU-003

Contextual documents cannot create operational facts.

24.9 Golden benchmark

The domain model must manually produce:

Plain Text
Do-nothing breached customer orders: 2
Do-nothing revenue at risk: ₹1,600,000
Hybrid intervention cost: ₹132,000
Hybrid breached customer orders: 0
Hybrid revenue protected: ₹1,600,000
Recommended intervention: Hybrid

These values remain provisional until the complete scheduling timeline is independently recalculated and frozen.

Deliverable
Plain Text
docs/domain/domain-test-catalogue.md
25. Phase 2U: Domain Review and Falsification
Goal

Actively attempt to break the model before generating data or code.

25.1 Review perspectives
Supply-chain review

Check:

Is the inventory logic plausible?
Are supplier constraints represented?
Can a recommendation violate physical reality?
Are delayed receipts calculated consistently?
Manufacturing review

Check:

Does production require all mandatory components?
Is facility capacity enforced?
Is completed production protected?
Does rescheduling harm other orders?
Financial review

Check:

Is revenue at risk overstated?
Is partial lateness handled?
Are incremental and total costs separated?
Are currencies consistent?
Temporal review

Check:

Are time intervals unambiguous?
Can records overlap?
Can future data leak into historical scenarios?
Are timezone conversions stable?
Causal review

Check:

Does every impact have an intermediate chain?
Are correlation and causation confused?
Can historical documents override structured facts?
Are contributing causes labelled properly?
25.2 Adversarial model scenarios
Scenario A: No impact

Supplier outage occurs, but sufficient inventory exists for the entire horizon.

Expected:

Plain Text
Affected supply: Yes
Operational shortage: No
SLA breaches: 0
Revenue at risk: ₹0
Scenario B: No feasible intervention
No transferable inventory
No approved alternate supplier
PO cannot be expedited
Production rescheduling cannot resolve shortage

Expected:

Plain Text
NO_FEASIBLE_INTERVENTION
Scenario C: Insufficient data

No valid inventory snapshot exists.

Expected:

Plain Text
INSUFFICIENT_DATA

Not:

Plain Text
0 inventory
Scenario D: Partial fulfilment

Only half the customer quantity can be delivered on time.

Expected:

Partial late quantity
Proportional revenue at risk
One breached order
Scenario E: Cheaper but worse intervention

An intervention has the lowest cost but more SLA breaches.

Expected:

It does not win under MINIMIZE_SLA_BREACHES.
Scenario F: Rescheduling externality

Moving one production order earlier delays another high-value order.

Expected:

Both benefit and harm are calculated.
Scenario G: Late-arriving correction

Inventory correction arrives after scenario completion.

Expected:

Original scenario remains unchanged.
A new scenario version may use the correction.
Scenario H: Identical candidates

Two candidates have identical metrics.

Expected:

Tie is reported.
Stable tie-breaker is used only if one recommendation is required.
25.3 Model consistency checks
Conservation of inventory

For every component and scenario:

EndingInventory=StartingInventory+Receipts+TransfersIn−Consumption−TransfersOutEndingInventory = StartingInventory + Receipts + TransfersIn - Consumption - TransfersOutEndingInventory=StartingInventory+Receipts+TransfersIn−Consumption−TransfersOut

Any unexplained difference is a failure.

Conservation of production
CompletedQuantity≤PlannedQuantityCompletedQuantity \le PlannedQuantityCompletedQuantity≤PlannedQuantity
Allocation conservation
∑AllocatedQuantity≤EligibleAvailableQuantity\sum AllocatedQuantity \le EligibleAvailableQuantity∑AllocatedQuantity≤EligibleAvailableQuantity
Revenue-at-risk bound
0≤RevenueAtRisk≤TotalOpenOrderRevenue0 \le RevenueAtRisk \le TotalOpenOrderRevenue0≤RevenueAtRisk≤TotalOpenOrderRevenue
Intervention-cost bound
InterventionCost≥0InterventionCost \ge 0InterventionCost≥0
Time ordering
ProjectedCompletion≥ProjectedStartProjectedCompletion \ge ProjectedStartProjectedCompletion≥ProjectedStart ProjectedDelivery≥ProjectedProductAvailabilityProjectedDelivery \ge ProjectedProductAvailabilityProjectedDelivery≥ProjectedProductAvailability
Deliverables
Plain Text
docs/domain/domain-review-report.md
docs/domain/adversarial-scenarios.md
docs/domain/invariant-catalogue.md
26. Phase 2 Quality Benchmarks
26.1 Domain completeness
DomainCompleteness=required Phase 1 concepts formally modelledtotal required Phase 1 conceptsDomainCompleteness = \frac{\text{required Phase 1 concepts formally modelled}} {\text{total required Phase 1 concepts}}DomainCompleteness=total required Phase 1 conceptsrequired Phase 1 concepts formally modelled​

Target:

Plain Text
100%
26.2 Formula coverage
FormulaCoverage=numerical product outputs with frozen formulasall numerical product outputsFormulaCoverage = \frac{\text{numerical product outputs with frozen formulas}} {\text{all numerical product outputs}}FormulaCoverage=all numerical product outputsnumerical product outputs with frozen formulas​

Target:

Plain Text
100%
26.3 Causal coverage
CausalCoverage=impact outputs with complete dependency pathsall impact outputsCausalCoverage = \frac{\text{impact outputs with complete dependency paths}} {\text{all impact outputs}}CausalCoverage=all impact outputsimpact outputs with complete dependency paths​

Target for golden scenario:

Plain Text
100%
26.4 Temporal coverage

All time-dependent entities must define:

Effective-time semantics
Scenario selection rule
Boundary behavior

Target:

Plain Text
100%
26.5 Invariant coverage

Each material domain entity must have at least one relevant validity invariant.

Target:

Plain Text
100%
26.6 Golden-scenario agreement
Agreement=independently matched golden outputstotal golden outputsAgreement = \frac{\text{independently matched golden outputs}} {\text{total golden outputs}}Agreement=total golden outputsindependently matched golden outputs​

Target:

Plain Text
100%
26.7 Ambiguity rate
AmbiguityRate=open material model ambiguitiesmaterial model decisionsAmbiguityRate = \frac{\text{open material model ambiguities}} {\text{material model decisions}}AmbiguityRate=material model decisionsopen material model ambiguities​

Required:

Plain Text
0% for Priority 0 behavior
26.8 Requirement traceability

Every Priority 0 Phase 1 requirement must map to:

Domain concept
Rule or formula
Domain test
Future implementation phase

Target:

Plain Text
100%
27. Phase 2 Scorecard
Category	Weight
Domain-language precision	8
Entity and relationship completeness	12
Temporal-model correctness	12
Inventory and allocation logic	12
BOM and production logic	12
Customer and financial logic	10
Causal-model completeness	12
Intervention and counterfactual model	10
Golden-scenario validation	8
Traceability and testability	4
Total	100
Passing threshold
Plain Text
95–100: Pass
90–94: Conditional pass
Below 90: Fail
Automatic failures

Phase 2 fails regardless of score if:

Baseline and do-nothing remain confused.
No deterministic inventory equation exists.
Revenue at risk remains undefined.
Missing data is treated as zero.
A recommendation can violate a hard constraint.
Operational facts can be modified by simulation.
Causal traces skip intermediate dependencies.
Scenario time semantics remain undefined.
Golden scenario cannot be manually solved.
Independent golden-scenario calculations disagree.
Partial fulfilment is possible but not modelled or explicitly prohibited.
Intervention cost double-counting remains unresolved.
Phase 3 would need to invent business rules.
28. Required Phase 2 Repository Structure
Plain Text
docs/domain/
├── phase-1-handoff-review.md
├── bounded-context.md
├── domain-glossary.md
├── conceptual-entity-model.md
├── relationship-model.md
├── dependency-graph.md
├── state-transition-model.md
├── units-and-financial-model.md
├── temporal-model.md
├── time-examples.md
├── disruption-model.md
├── inventory-model.md
├── allocation-policy.md
├── bom-model.md
├── material-requirement-formulas.md
├── production-scheduling-model.md
├── production-priority-policy.md
├── customer-fulfilment-model.md
├── sla-and-revenue-model.md
├── causal-model.md
├── causal-edge-catalogue.md
├── causal-trace-format.md
├── intervention-model.md
├── feasibility-rule-catalogue.md
├── counterfactual-model.md
├── formula-catalogue.md
├── objective-and-ranking-model.md
├── provenance-model.md
├── uncertainty-and-data-quality-model.md
├── invariant-catalogue.md
├── adversarial-scenarios.md
├── domain-test-catalogue.md
├── domain-review-report.md
├── phase-2-traceability-matrix.csv
├── phase-2-completion-report.md
└── golden-scenario/
├── scenario-definition.md
├── input-records.csv
├── manual-calculation.md
├── do-nothing-result.json
├── intervention-results.json
├── expected-recommendation.json
├── causal-traces.md
└── assumptions.md
29. Phase 2 Traceability Matrix

Create:

Plain Text
docs/domain/phase-2-traceability-matrix.csv

Recommended columns:

Plain Text
phase1_requirement_id
domain_concept
entity
relationship
rule_id
formula_id
invariant_id
domain_test_id
golden_scenario_evidence
future_phase
status
notes

Example:

Plain Text
FR-IMP-012,
Revenue at risk,
CustomerOrderLine,
CustomerOrderLine-to-ProductionOrder,
SLA-004,
FIN-006,
INV-FIN-003,
DT-CUS-002,
golden-scenario/manual-calculation.md,
Phase 5,
APPROVED,
Late quantity only
30. Phase 2 Execution Order

Follow this sequence. Do not begin with the golden scenario before the basic language, time and calculation rules are stable.

Work Block 1: Handoff and language
Plain Text
2A. Validate Phase 1 inputs
2B. Lock bounded context
2B. Freeze domain glossary
2B. Resolve overloaded terms
Work Block 2: Structural model
Plain Text
2C. Define entities
2C. Define value objects
2D. Define relationships
2D. Define cardinalities
2E. Define lifecycle states
Work Block 3: Measure and time
Plain Text
2F. Lock units
2F. Lock currency
2F. Lock rounding
2G. Define time dimensions
2G. Define effective intervals
2G. Define scenario as-of semantics
2G. Define simulation horizon
Work Block 4: Operational rules
Plain Text
2H. Define supplier-outage behavior
2I. Define inventory position
2I. Define allocation policy
2I. Define shortage rule
2J. Define BOM selection
2J. Define material requirements
2K. Define production scheduling
2L. Define customer fulfilment
2L. Define SLA and revenue rules
Work Block 5: Causality and actions
Plain Text
2M. Build causal graph
2M. Define each causal edge
2M. Define causal traces
2N. Define interventions
2N. Define feasibility rules
2O. Define scenario overlays
2O. Define candidate isolation
Work Block 6: Metrics and evidence
Plain Text
2P. Freeze formulas
2P. Freeze objectives
2P. Freeze ranking logic
2Q. Define provenance
2R. Define data-quality states
2R. Define uncertainty labels
Work Block 7: Golden scenario
Plain Text
2S. Create minimal operational state
2S. Calculate no-disruption baseline
2S. Apply supplier outage
2S. Calculate do-nothing impact
2S. Calculate each intervention
2S. Select expected recommendation
2S. Independently verify calculations
Work Block 8: Falsification
Plain Text
2T. Write domain tests
2U. Run adversarial walkthroughs
2U. Check conservation invariants
2U. Resolve contradictions
2U. Freeze Phase 2 specification
Work Block 9: Handoff
Plain Text
2V. Complete traceability matrix
2V. Write completion report
2V. Freeze Phase 3 data requirements
2V. Tag Phase 2 documentation version
31. Phase 2 Final Gate Checklist
Language and scope
 Bounded context is explicit.
 Domain glossary is complete.
 Baseline and do-nothing are distinct.
 Revenue at risk and loss are distinct.
 Facts, projections and assumptions are distinguishable.
Entity model
 Every core entity has an identifier.
 Every important attribute has a business meaning.
 Cardinalities are documented.
 Versioned relationships are explicit.
 Value objects contain their units.
Temporal model
 Event time is defined.
 Reported time is defined.
 Effective time is defined.
 Scenario as-of time is defined.
 Simulation horizon is defined.
 Time zone policy is defined.
 Boundary intervals are defined.
 Late-arriving data behavior is defined.
Inventory and BOM
 Available inventory formula is frozen.
 Projected balance formula is frozen.
 Allocation priority is frozen.
 Transferable quantity is defined.
 Shortage date is defined.
 BOM selection rule is defined.
 Component requirement formula is frozen.
 Partial production policy is explicit.
Production and customer impact
 Material-ready time is defined.
 Capacity-ready time is defined.
 Production delay is defined.
 Projected delivery is defined.
 SLA breach is defined.
 Partial fulfilment behavior is defined.
 Revenue-at-risk formula is frozen.
Causality
 Causal graph is complete.
 Every edge has a rule.
 Every impact can trace to source records.
 Contextual evidence cannot create operational facts.
 No direct unsupported jump to revenue impact exists.
Interventions
 Do-nothing is defined.
 Inventory transfer is defined.
 Expedition is defined.
 Alternate supply is defined.
 Rescheduling is defined.
 Hybrid intervention is defined.
 Feasibility reasons are defined.
 Hard and soft constraints are separated.
Counterfactual model
 Baseline state is immutable.
 Disruption overlay is fixed per scenario.
 Candidate overlays are isolated.
 Comparison basis is common.
 Outcome deltas name their reference case.
 Deterministic replay is defined.
Measures and evidence
 All numerical outputs have formulas.
 All formulas have units.
 Cost components are non-overlapping.
 Provenance model is complete.
 Missing values are not treated as zero.
 Confidence classifications are evidence-based.
Golden scenario
 Input state is complete.
 No-disruption baseline is calculated.
 Do-nothing result is calculated.
 Every intervention is calculated.
 Expected recommendation is calculated.
 Causal traces are complete.
 Two independent calculations agree.
 Golden JSON outputs are frozen.
Quality
 Domain completeness is 100%.
 Formula coverage is 100%.
 Causal coverage is 100%.
 Priority 0 ambiguity is 0%.
 Traceability coverage is 100%.
 Phase 2 score is at least 95.
 No automatic-failure condition remains.
32. Phase 2V: Phase 3 Handoff
Phase 3 name

Dataset Engineering and Ground-Truth Construction

Goal of the handoff

Phase 3 must generate data that obeys the Phase 2 model. It must not introduce new business rules.

Mandatory Phase 3 inputs
Structural inputs
Entity catalogue
Attribute definitions
Relationships
Cardinalities
State transitions
Effective-time rules
Quantitative inputs
Units
Currency
Quantity precision
Cost formulas
Revenue formulas
Capacity formulas
Lead-time rules
Causal inputs
Disruption behavior
Inventory propagation
BOM requirements
Production scheduling
Customer impact
Intervention overlays
Validation inputs
Domain invariants
Rejection codes
Domain tests
Golden scenario
Adversarial scenarios
Benchmark inputs
Expected no-impact case
Expected no-feasible-plan case
Expected insufficient-data case
Expected partial-fulfilment case
Expected golden recommendation
Phase 3 must produce
Data-generation specification
Synthetic-data generator
Seed dataset
Data dictionary
Data-quality validator
Golden dataset
Benchmark scenario suite
Ground-truth outcomes
Dataset statistics
Dataset reproducibility report
Final Phase 2 Outcome

When Phase 2 passes, ChronosDB will no longer have vague statements such as:

“The AI determines the impact.”
“The system predicts revenue risk.”
“The simulator finds the best action.”

Instead, it will have defensible statements:

A supplier outage changes defined outstanding receipts.
Changed receipts alter projected component balances.
Negative availability produces shortages at known timestamps.
Mandatory shortages delay production under explicit scheduling rules.
Production delay changes product availability and projected delivery.
Late quantity creates proportionate revenue at risk.
Interventions modify isolated future-state overlays.
Hard constraints remove infeasible candidates.
A frozen objective ranks the remaining candidates.
Every output has a complete causal and provenance chain.

The next phase is:

Phase 3: Dataset Engineering and Ground-Truth Construction

That phase will convert the locked Phase 2 model into a realistic, reproducible synthetic supply-chain dataset and a frozen benchmark suite.