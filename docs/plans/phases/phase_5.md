Phase 5 Deep Dive: Deterministic Impact Engine
Calculate the Cascading Impact of Supply-Chain Disruptions

Phase 4 produced the coherent demonstration dataset and frozen ground truth. Phase 5 now builds the first major computational core of ChronosDB: a deterministic engine that traces a disruption from delayed supply through inventory, manufacturing, customer commitments, SLA exposure, and revenue at risk.

This engine must function without an LLM. Given the same state, disruption, horizon, and rule version, it must always produce exactly the same result, including its intermediate calculations and causal evidence.

1. Phase Definition
Phase name

Deterministic Impact Engine

Primary goal

Implement a deterministic calculation engine that answers:

If this supplier disruption occurs and no recovery intervention is applied, what exactly will be affected, when will the effects occur, and why?

Required result

At the end of Phase 5, the system must calculate:

Affected purchase orders
Delayed or unavailable component receipts
Projected inventory states
Component shortage times and quantities
Affected production batches and orders
Material-ready times
Capacity-ready times
Projected production starts and completions
Affected customer-order lines
Projected delivery times
SLA breaches
Late quantities
Revenue at risk
Complete causal traces
Calculation provenance
Deterministic do-nothing results
Core transformation
Plain Text
Frozen operational state
+
Supplier disruption
+
Business-rule version
+
Simulation horizon
↓
Affected inbound supply
↓
Projected inventory timeline
↓
Material shortages
↓
Production schedule impact
↓
Customer fulfilment impact
↓
SLA breaches
↓
Revenue at risk
↓
Auditable causal trace
2. Phase 5 Definition of Done

Phase 5 is complete only when:

Given the frozen Phase 4 dataset, a validated supplier-outage scenario, an as-of timestamp, and a simulation horizon, the engine deterministically produces the exact expected do-nothing impact, preserves every intermediate calculation, explains the complete causal chain, and matches the frozen benchmark ground truth without using an LLM.

3. Phase 5 Boundaries
In scope
Scenario-input validation
Historical-state reconstruction interface
Supplier-outage application
Purchase-order impact calculation
Inventory-event projection
Material-allocation calculation
Shortage detection
BOM explosion
Production scheduling
Customer fulfilment
SLA classification
Revenue-at-risk calculation
Causal graph generation
Calculation provenance
Partial-result handling
Deterministic replay
Golden-scenario verification
Benchmark evaluation
Performance measurement
Failure diagnostics
Out of scope
Recovery-intervention simulation
Candidate generation
Intervention optimization
Vector retrieval
LLM planning
LLM narration
Final user interface
Autonomous operational actions
Probabilistic forecasting
Monte Carlo simulation
Live ERP updates
Multi-disruption optimization

Phase 5 computes the do-nothing impact under the disruption. Phase 6 will apply counterfactual interventions.

4. Phase 5 Structure
Plain Text
Phase 5
├── 5A. Phase 4 handoff and ground-truth validation
├── 5B. Engine contract and deterministic boundaries
├── 5C. Input and output model
├── 5D. Rule registry and version control
├── 5E. Operational-state reconstruction
├── 5F. Disruption-impact resolver
├── 5G. Inbound-supply projection
├── 5H. Inventory timeline engine
├── 5I. Material requirement and allocation engine
├── 5J. Shortage detection engine
├── 5K. Production scheduling engine
├── 5L. Customer fulfilment engine
├── 5M. SLA and revenue-impact engine
├── 5N. Causal trace and provenance engine
├── 5O. Partial-result and data-quality handling
├── 5P. Idempotency, replay, and determinism
├── 5Q. Persistence and execution ledger
├── 5R. Golden-scenario implementation
├── 5S. Benchmark and correctness evaluation
├── 5T. Performance and scalability evaluation
├── 5U. Testing and adversarial validation
├── 5V. Observability and diagnostics
├── 5W. Independent review and release gate
└── 5X. Phase 6 handoff
5. Phase 5A: Phase 4 Handoff and Ground-Truth Validation
Goal

Confirm that the impact engine is being built against the frozen dataset and not against changing sample data.

Required inputs
Plain Text
chronosdb-demo-dataset-v1.0.0
dataset manifest
dataset checksums
load-order manifest
golden scenario
60 benchmark scenarios
expected do-nothing outcomes
negative fixtures
temporal replay expectations
domain formula catalogue
causal edge catalogue
Required loaded data

The engine requires access to:

Suppliers
Supplier-component agreements
Components
Products
BOM versions and lines
Warehouses
Facilities
Transfer lanes, for later phases
Inventory events and snapshots
Purchase orders and receipts
Production orders and batches
Customer orders and lines
Production-customer allocations
Facility capacity calendars
Disruption events
Scenario definitions
Rule metadata
Ground-truth intake validation

For every benchmark scenario:

Input-state hash exists.
As-of timestamp exists.
Simulation horizon exists.
Expected do-nothing result exists.
Expected causal roots exist.
Expected data-quality status exists.
Expected output uses the same rule version.
Scenario belongs to one valid partition.
Initial command contract
Shell
make impact-intake-check
make impact-golden-input-check
make impact-benchmark-manifest-check
Deliverable
Plain Text
docs/impact-engine/phase-4-handoff-review.md
Exit gate
Dataset checksums match.
Golden source records match the frozen release.
Test outcomes have not been modified.
Engine rule semantics match Phase 2.
No benchmark field is ambiguous.
The implementation cannot read expected outputs at runtime.
6. Phase 5B: Engine Contract and Deterministic Boundaries
Goal

Define the impact engine as a pure, reproducible business calculation.

Conceptual signature
Python
ImpactResult calculate_impact(
OperationalState state,
Disruption disruption,
SimulationHorizon horizon,
RuleSet rules
)
Deterministic input contract

The result may depend only on:

Operational-state version
Scenario as-of time
Disruption definition
Simulation horizon
Rule-set version
Allocation policy
Scheduling policy
Calendar configuration

The result must not depend on:

Current wall-clock time
Thread execution order
Unseeded randomness
LLM output
Network calls
Mutable global state
Database row-return order without explicit sorting
Locale-dependent date or number processing
Architectural principle

Separate:

Domain calculation

Pure calculation over typed objects.

Data access

Loads and verifies operational state.

Persistence

Stores execution records and results.

Presentation

Formats impact results for API or UI use.

The calculation layer should not contain SQL queries or HTTP concerns.

Recommended module boundaries
Plain Text
src/backend/chronosdb/impact/
├── contracts/
├── rules/
├── state/
├── disruption/
├── supply/
├── inventory/
├── materials/
├── production/
├── fulfilment/
├── financial/
├── causality/
├── provenance/
├── validation/
└── orchestration/
Deliverable
Plain Text
docs/impact-engine/engine-contract.md
7. Phase 5C: Input and Output Model
Goal

Define precise typed contracts for engine execution.

7.1 Impact request
JSON
{
"scenario_id": "SCN-GOLD-001",
"as_of_time": "2026-11-11T02:30:00Z",
"simulation_end_time": "2026-12-11T02:30:00Z",
"disruption_event_id": "EVT-GOLD-001",
"rule_set_version": "impact-rules-v1.0.0",
"allocation_policy": "priority-due-date-v1",
"scheduling_policy": "batch-capacity-v1"
}
7.2 Input-state identity
JSON
{
"dataset_version": "1.0.0",
"state_version": "STATE-GOLD-001",
"state_hash": "sha256-value",
"as_of_time": "2026-11-11T02:30:00Z"
}
7.3 Top-level impact result
JSON
{
"impact_run_id": "IR-...",
"scenario_id": "SCN-GOLD-001",
"status": "COMPLETED",
"data_quality_status": "COMPLETE",
"rule_set_version": "impact-rules-v1.0.0",
"input_state_hash": "...",
"result_hash": "...",
"affected_purchase_orders": [],
"affected_components": [],
"inventory_timelines": [],
"shortages": [],
"affected_production_orders": [],
"affected_customer_orders": [],
"headline_metrics": {},
"causal_traces": [],
"warnings": [],
"errors": [],
"provenance": {}
}
7.4 Headline metrics
JSON
{
"affected_supplier_count": 1,
"affected_purchase_order_count": 1,
"supply_affected_component_count": 1,
"shortage_affected_component_count": 1,
"affected_production_order_count": 2,
"affected_customer_order_count": 2,
"sla_breached_customer_order_count": 2,
"late_quantity": 400,
"total_delay_unit_hours": 110400,
"maximum_delay_hours": 288,
"revenue_at_risk": {
"amount": "1600000.00",
"currency": "INR"
}
}

The exact delay values must come from the frozen golden timeline.

7.5 Status values
Plain Text
PENDING
VALIDATING
RECONSTRUCTING_STATE
APPLYING_DISRUPTION
PROJECTING_INVENTORY
SCHEDULING_PRODUCTION
CALCULATING_CUSTOMER_IMPACT
BUILDING_PROVENANCE
COMPLETED
PARTIALLY_COMPLETED
REJECTED
FAILED
Deliverables
Plain Text
docs/impact-engine/input-contract.md
docs/impact-engine/output-contract.md
schemas/impact-request.schema.json
schemas/impact-result.schema.json
8. Phase 5D: Rule Registry and Version Control
Goal

Make every business calculation explicit and versioned.

Rule categories
Plain Text
STATE
SUPPLY
INVENTORY
BOM
ALLOCATION
PRODUCTION
FULFILMENT
SLA
FINANCIAL
CAUSAL
QUALITY
Rule identifier pattern
Plain Text
STATE-001
SUP-001
INV-001
BOM-001
ALLOC-001
PROD-001
FUL-001
SLA-001
FIN-001
CAU-001
DQ-001
xample rule definition
YAML
rule_id: INV-004
name: projected_inventory_balance
version: 1.0.0
description: >
Calculates projected component balance using opening inventory,
eligible receipts and ordered consumption events.
inputs:
- opening_available_quantity
- receipt_events
- consumption_events
- transfer_events
formula: >
prior_balance + receipts + transfers_in -
consumption - transfers_out
output:
- projected_balance
rounding: none
failure_condition:
- missing_opening_state
Rule-set manifest
JSON
{
"rule_set_version": "impact-rules-v1.0.0",
"domain_model_version": "2.0",
"dataset_compatibility": ["1.0.0"],
"rules": [
"STATE-001@1.0.0",
"SUP-001@1.0.0",
"INV-004@1.0.0"
]
}
Version rules
Patch

Implementation correction that does not alter intended business semantics.

Minor

Backward-compatible rule addition.

Major

Changed business semantics or changed benchmark outcomes.

A changed formula that alters frozen expected outputs requires:

New rule-set version
New benchmark review
Potential new dataset or expected-outcome version
Release notes
Deliverables
Plain Text
config/rules/impact-rules-v1.0.0.yaml
docs/impact-engine/rule-catalogue.md
Exit gate
Every computed field references a rule.
Every rule has typed inputs and outputs.
Rounding is defined.
Edge cases are defined.
Rule-set compatibility is recorded.
Hidden business logic in presentation code is prohibited.
9. Phase 5E: Operational-State Reconstruction
Goal

Create the exact state known and valid at the scenario's as-of timestamp.

State-input classes
Effective master data
Active suppliers
Active agreements
Active products
Active BOM versions
Active SLA policies
Operational state
Inventory
Outstanding purchase orders
Production status
Customer-order status
Facility capacity
Information state

Records known by the system at the scenario time.

State-selection rule

A record is eligible when:

effective_from≤as_of<effective_toeffective\_from \le as\_of < effective\_toeffective_from≤as_of<effective_to

and:

ingested_time≤as_ofingested\_time \le as\_ofingested_time≤as_of

when information-time control applies.

Inventory reconstruction

Recommended approach:

Load latest valid checkpoint at or before as_of_time.
Apply ledger events after the checkpoint and through as_of_time.
Reconcile the calculated state.
Compare with an available benchmark snapshot when present.
Fail or warn on unexplained mismatch.
Purchase-order reconstruction

At the scenario time, determine:

Ordered quantity
Received quantity
Outstanding quantity
Current expected arrival
Current status
Active supplier
Destination warehouse
Production reconstruction

Determine:

Planned quantity
Completed quantity
Remaining quantity
Material previously issued
Current state
Locked batches
Future material demand
Customer reconstruction

Determine:

Open quantity
Fulfilled quantity
Remaining quantity
Promised time
Associated production demand
Priority
State hash

Canonicalize all impact-relevant records:

Plain Text
sort records by entity type and stable identifier
normalize timestamps to UTC
normalize decimal serialization
remove non-semantic metadata
serialize deterministically
calculate SHA-256
State-reconstruction result
JSON
{
"state_version": "STATE-GOLD-001",
"as_of_time": "...",
"state_hash": "...",
"record_counts": {},
"completeness": "COMPLETE",
"warnings": []
}
Deliverables
Plain Text
src/backend/chronosdb/impact/state/
docs/impact-engine/state-reconstruction.md
Acceptance criteria
Golden-state hash matches Phase 4.
Ten historical reconstruction fixtures match exactly.
Late-arriving data is excluded when appropriate.
Expired BOM and agreements are excluded.
No future event leaks into the reconstructed state.
10. Phase 5F: Disruption-Impact Resolver
Goal

Determine exactly which inbound commitments are affected by the supplier outage.

Processing sequence
Validate disruption.
Resolve supplier.
Resolve scope.
Select outstanding purchase orders.
Exclude already received quantities.
Apply outage interval.
Apply recovery lag.
Generate changed receipt events.
Preserve original and disrupted values.
Produce impact evidence.
Affected purchase-order condition

A purchase order is affected when:

Supplier matches.
It has outstanding quantity.
Status is eligible.
Scope includes its component or ID.
Expected supply intersects the outage rule.
It was not fully received before the outage.
Outstanding quantity
Qoutstanding=max⁡(0,Qordered−Qreceived)Q_{outstanding} = \max(0, Q_{ordered} - Q_{received})Qoutstanding​=max(0,Qordered​−Qreceived​)
Disrupted arrival

For the locked Phase 2 rule:

Arrivaldisrupted=max⁡(Arrivaloriginal,OutageEnd+RecoveryLag)Arrival_{disrupted} = \max( Arrival_{original}, OutageEnd + RecoveryLag )Arrivaldisrupted​=max(Arrivaloriginal​,OutageEnd+RecoveryLag)
Purchase-order impact object
JSON
{
"purchase_order_id": "PO-2208",
"component_id": "CMP-MCU-42",
"outstanding_quantity": "800",
"original_arrival": "2026-11-13T00:00:00Z",
"disrupted_arrival": "2026-11-27T00:00:00Z",
"delay_hours": 336,
"rule_id": "SUP-004",
"source_record_ids": ["PO-2208", "EVT-GOLD-001"]
}
Edge cases
Partially received purchase order
Arrival exactly at outage start
Arrival exactly at outage end
Cancelled purchase order
Component-scoped outage
Purchase-order-scoped outage
Supplier agreement expires during horizon
Recovery extends beyond simulation horizon
Deliverables
Plain Text
src/backend/chronosdb/impact/disruption/
src/backend/chronosdb/impact/supply/
docs/impact-engine/disruption-resolution.md
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
15. Phase 5K: Production Scheduling Engine
Goal

Convert material availability and facility capacity into projected manufacturing timelines.

Scheduling model

For each production batch:

ProjectedStart=max⁡(PlannedStart,MaterialReadyTime,CapacityReadyTime)ProjectedStart = \max( PlannedStart, MaterialReadyTime, CapacityReadyTime )ProjectedStart=max(PlannedStart,MaterialReadyTime,CapacityReadyTime) ProjectedCompletion=ProjectedStart+ProcessingDurationProjectedCompletion = ProjectedStart + ProcessingDurationProjectedCompletion=ProjectedStart+ProcessingDuration ProductionDelay=max⁡(0,ProjectedCompletion−PlannedCompletion)ProductionDelay = \max( 0, ProjectedCompletion - PlannedCompletion )ProductionDelay=max(0,ProjectedCompletion−PlannedCompletion)
Batch model

Golden scenario:

Plain Text
Batch size: 100 finished units
Capacity use: 100 finished units per calendar day
Material issue: batch start
Duration: 24 hours for one 100-unit batch
Scheduling queue

Order batches by:

Already in progress
Released status
Explicit production priority
Highest linked customer priority
Earliest promised date
Planned start
Stable order and batch ID
Facility capacity

For each time bucket:

AllocatedCapacityt≤EffectiveCapacitytAllocatedCapacity_t \le EffectiveCapacity_tAllocatedCapacityt​≤EffectiveCapacityt​

A production batch may not overlap unavailable capacity unless partial-capacity processing is explicitly supported.

No artificial deadlock

Because material availability depends on production allocation and scheduling, implement a clear sequence:

Load fixed in-progress commitments.
Build candidate order queue.
For each batch in priority order:
Determine earliest material-ready time.
Determine earliest capacity-ready time.
Select projected start.
Consume material at projected start.
Reserve capacity.
Calculate completion.
Continue until horizon end.
Projected production result
JSON
{
"production_order_id": "MO-0882",
"planned_start": "...",
"planned_completion": "...",
"projected_start": "...",
"projected_completion": "...",
"delay_hours": 288,
"blocking_components": ["CMP-MCU-42"],
"blocking_receipts": ["PO-2208"],
"batches": []
}
Horizon behavior

If material or capacity does not become available:

Plain Text
projected_start: null
projected_completion: null
status: NOT_COMPLETED_WITHIN_HORIZON

Do not invent a completion date beyond available information unless the event schedule supports it.

Deliverables
Plain Text
src/backend/chronosdb/impact/production/
docs/impact-engine/production-scheduling.md
Acceptance criteria
Golden scheduling timeline matches the frozen expected timeline.
Facility capacity is never exceeded.
Material is consumed exactly once.
Stable tie-breaking produces repeatable schedules.
Delaying one order can correctly affect later orders.

16. Phase 5L: Customer Fulfilment Engine
Goal

Map projected production output to customer-order fulfilment.

Fulfilment inputs
Customer-order lines
Unfulfilled quantities
Linked production orders
Finished inventory, if modelled
Product availability
Customer priority
Promised delivery
Delivery lead time
Allocation priority
Explicit customer priority
SLA class
Promised delivery time
Order time
Stable order-line ID
Product availability events

Each completed production batch creates:

Plain Text
product_id
quantity
availability_time
production_batch_id
facility_id
On-time quantity

Quantity available early enough to meet delivery commitment:

OnTimeQuantityl=min⁡(OpenQuantityl,EligibleQuantityAvailableByCutoffl)OnTimeQuantity_l = \min( OpenQuantity_l, EligibleQuantityAvailableByCutoff_l )OnTimeQuantityl​=min(OpenQuantityl​,EligibleQuantityAvailableByCutoffl​)
Late quantity
LateQuantityl=max⁡(0,OpenQuantityl−OnTimeQuantityl)LateQuantity_l = \max( 0, OpenQuantity_l - OnTimeQuantity_l )LateQuantityl​=max(0,OpenQuantityl​−OnTimeQuantityl​)
Projected delivery
ProjectedDeliveryl=ProductAvailabilityTimel+DeliveryLeadTimelProjectedDelivery_l = ProductAvailabilityTime_l + DeliveryLeadTime_lProjectedDeliveryl​=ProductAvailabilityTimel​+DeliveryLeadTimel​

For partial fulfilment, preserve multiple fulfilment segments:

JSON
{
"order_line_id": "COL-0704-01",
"segments": [
{
"quantity": 100,
"projected_delivery": "..."
},
{
"quantity": 100,
"projected_delivery": "..."
}
]
}
No double fulfilment
∑FulfilledQuantitysegments≤OpenOrderLineQuantity\sum FulfilledQuantity_{segments} \le OpenOrderLineQuantity∑FulfilledQuantitysegments​≤OpenOrderLineQuantity
Deliverables
Plain Text
src/backend/chronosdb/impact/fulfilment/
docs/impact-engine/customer-fulfilment.md
17. Phase 5M: SLA and Revenue-Impact Engine
Goal

Calculate business exposure from projected customer fulfilment.

SLA status

For each delivery segment:

Plain Text
ON_TIME
BREACHED
INSUFFICIENT_DATA

Optional warning state:

Plain Text
AT_RISK

AT_RISK must not be counted as an actual projected breach unless the formal policy says so.

Delay calculation
DelayHoursl=max⁡(0,ProjectedDeliveryl−PromisedDeliveryl)DelayHours_l = \max( 0, ProjectedDelivery_l - PromisedDelivery_l )DelayHoursl​=max(0,ProjectedDeliveryl​−PromisedDeliveryl​)
Revenue at risk
RevenueAtRiskl=LateQuantityl×UnitRevenuelRevenueAtRisk_l = LateQuantity_l \times UnitRevenue_lRevenueAtRiskl​=LateQuantityl​×UnitRevenuel​
Total revenue at risk
TotalRevenueAtRisk=∑lRevenueAtRisklTotalRevenueAtRisk = \sum_l RevenueAtRisk_lTotalRevenueAtRisk=l∑​RevenueAtRiskl​
Quantity-weighted delay
WeightedDelayHours=∑lLateQuantityl×DelayHourslWeightedDelayHours = \sum_l LateQuantity_l \times DelayHours_lWeightedDelayHours=l∑​LateQuantityl​×DelayHoursl​
Breach metrics

Report:

Breached order-line count
Breached customer-order count
Late product quantity
Revenue at risk
Maximum delay
Average delay among late segments
Quantity-weighted delay
Revenue bounds

For every line:

0≤RevenueAtRiskl≤OpenQuantityl×UnitRevenuel0 \le RevenueAtRisk_l \le OpenQuantity_l \times UnitRevenue_l0≤RevenueAtRiskl​≤OpenQuantityl​×UnitRevenuel​
Golden expected headline

The locked Phase 4 result should produce:

Plain Text
Breached customer orders: 2
Revenue at risk: ₹1,600,000

All detailed timing and delay values must match the frozen expected timeline exactly.

Deliverables
Plain Text
src/backend/chronosdb/impact/financial/
src/backend/chronosdb/impact/fulfilment/sla.py
docs/impact-engine/sla-and-financial-impact.md
18. Phase 5N: Causal Trace and Provenance Engine
Goal

Explain exactly how each impact was produced.

Causal node types
Plain Text
DISRUPTION
PURCHASE_ORDER
RECEIPT_CHANGE
INVENTORY_STATE
SHORTAGE
MATERIAL_ALLOCATION
PRODUCTION_BATCH
PRODUCTION_ORDER
PRODUCT_AVAILABILITY
CUSTOMER_ORDER_LINE
SLA_BREACH
REVENUE_AT_RISK
Causal edge types
Plain Text
AFFECTS
DELAYS
REDUCES
CAUSES_SHORTAGE
BLOCKS
RESCHEDULES
PRODUCES
FULFILLS
BREACHES
EXPOSES_REVENUE
Golden trace example
Plain Text
EVT-GOLD-001
SUP-0104 outage
↓ DELAYS
PO-2208
800 MCU receipt delayed to 27 Nov
↓ REDUCES
WH-PUNE projected MCU availability
↓ CAUSES_SHORTAGE
CMP-MCU-42 shortage
↓ BLOCKS
MO-0882 and MO-0889
↓ DELAYS
Product availability
↓ DELAYS
CO-0704 and CO-0711
↓ BREACHES
Customer SLA commitments
↓ EXPOSES_REVENUE
₹1,600,000 revenue at risk
Provenance object

Every impact metric should include:

Plain Text
metric ID
metric name
value
unit
currency if applicable
rule ID
rule version
input record IDs
calculation step IDs
scenario ID
impact run ID
state hash
timestamp
data-quality status
Causal trace validation

Every breached customer-order line must trace to:

At least one production constraint
At least one material or capacity cause
At least one upstream operational record
The disruption event when disruption caused the impact
Counterfactual causal comparison

Phase 5 should preserve a no-disruption reference calculation where possible.

This permits distinction between:

Plain Text
Already late before disruption
Newly late because of disruption
Made later by disruption
Unaffected

This is important because ChronosDB must not attribute pre-existing lateness to the supplier outage.

Attribution classes
Plain Text
DISRUPTION_CAUSED
DISRUPTION_WORSENED
PRE_EXISTING
UNRELATED
INSUFFICIENT_EVIDENCE
Deliverables
Plain Text
src/backend/chronosdb/impact/causality/
src/backend/chronosdb/impact/provenance/
docs/impact-engine/causality-and-provenance.md
Target
Plain Text
Causal coverage for golden and benchmark key outputs: 100%
19. Phase 5O: Partial-Result and Data-Quality Handling
Goal

Return safe, truthful output when some calculations cannot be completed.

Data-quality statuses
Plain Text
COMPLETE
PARTIAL_NONCRITICAL
PARTIAL_CRITICAL
INVALID
Impact-run statuses
Plain Text
COMPLETED
PARTIALLY_COMPLETED
REJECTED
FAILED
Critical missing data examples
No inventory state
No active BOM
Missing component unit
Missing customer promised date
Missing production-customer relationship
Inconsistent production quantity
Unknown supplier
Invalid disruption interval
Noncritical missing data examples
Missing descriptive supplier name
Missing historical incident
Missing optional notes
Missing nonessential classification
Failure-isolation behavior

If one customer line lacks a promised date:

Mark that line INSUFFICIENT_DATA.
Continue calculating other lines.
Exclude the unknown line from numerical SLA totals or report it separately.
Do not treat the line as on time.
Do not treat revenue at risk as zero.
Mark run PARTIALLY_COMPLETED.
Error object
JSON
{
"code": "MISSING_PROMISED_DELIVERY",
"severity": "CRITICAL_FOR_ENTITY",
"entity_type": "CUSTOMER_ORDER_LINE",
"entity_id": "COL-...",
"affected_outputs": [
"sla_status",
"delay_hours",
"revenue_at_risk"
],
"message": "Promised delivery is required for SLA calculation."
}
Deliverables
Plain Text
src/backend/chronosdb/impact/validation/
docs/impact-engine/data-quality-and-partial-results.md
20. Phase 5P: Idempotency, Replay, and Determinism
Goal

Guarantee stable and reproducible results.

Execution identity

Construct a deterministic execution key from:

Plain Text
scenario ID
state hash
disruption hash
simulation horizon
rule-set version
allocation policy
scheduling policy
Request fingerprint
Fingerprint=SHA256(CanonicalRequest+StateHash+RuleSetVersion)Fingerprint = SHA256( CanonicalRequest + StateHash + RuleSetVersion )Fingerprint=SHA256(CanonicalRequest+StateHash+RuleSetVersion)
Idempotency behavior

When the same fingerprint is submitted:

Return the existing completed result, or
Recalculate and confirm the same result hash in explicit verification mode

Do not create conflicting duplicate results.

Result hash

Canonicalize:

All deterministic output fields
Stable array ordering
UTC timestamps
Decimal strings
Explicit nulls
Rule versions

Exclude:

Execution duration
Runtime host ID
Log correlation ID
Creation timestamp, if it is not business-semantic
Determinism benchmark

Run the golden scenario:

Plain Text
100 times

Target:

Plain Text
Unique business result hashes: 1
Value mismatches: 0
Ordering mismatches: 0

Run a representative set of 20 benchmark scenarios:

Plain Text
10 times each

Target:

Plain Text
200/200 stable result hashes
Cross-process test

Run the same scenario:

In separate processes
After service restart
With different thread scheduling
After database restart

Expected business result remains identical.

Deliverables
Plain Text
docs/impact-engine/determinism-contract.md
artifacts/phase-5/determinism-report.json
21. Phase 5Q: Persistence and Execution Ledger
Goal

Persist inputs, intermediate calculations, outputs, and errors without mutating operational truth.

Conceptual result records
Plain Text
IMPACT_RUN
IMPACT_RUN_INPUT
AFFECTED_SUPPLY
PROJECTED_INVENTORY_EVENT
COMPONENT_SHORTAGE
PRODUCTION_IMPACT
CUSTOMER_IMPACT
IMPACT_METRIC
CAUSAL_NODE
CAUSAL_EDGE
CALCULATION_TRACE
IMPACT_WARNING
IMPACT_ERROR

The physical Db2 schema may already exist or may be implemented alongside this phase, but the engine contract remains independent.

Run record
Plain Text
impact_run_id
scenario_id
request_fingerprint
input_state_hash
rule_set_version
status
started_at
completed_at
result_hash
data_quality_status
error_summary
Persistence rules
Operational source records are read-only.
Projected events are stored separately.
Intermediate calculations are linked to an impact run.
Failed runs preserve diagnostics.
Repeated execution does not overwrite historical runs.
Completed results are immutable under the application role.
Verification reruns create a linked verification record or reuse prior output.
Transaction boundary

Recommended:

Create impact-run record.
Freeze input references.
Perform domain calculation outside long database transaction.
Persist result atomically.
Mark run complete.
If persistence fails, retain enough diagnostics to retry safely.
Deliverables
Plain Text
src/backend/chronosdb/impact/persistence/
docs/impact-engine/execution-ledger.md
22. Phase 5R: Golden-Scenario Implementation
Goal

Make the frozen golden scenario pass exactly before evaluating the broad suite.

Golden execution steps
Step 1: Reconstruct state

As of:

Plain Text
11 Nov 2026, 08:00 IST

Verify:

Plain Text
WH-PUNE CMP-MCU-42 available: 400
WH-CHENNAI CMP-MCU-42:
700 on hand
180 protected local demand
120 safety stock
400 transferable, although transfer is not applied in Phase 5
Step 2: Apply disruption
Plain Text
SUP-0104 unavailable for 14 days
Recovery lag: 2 days
PO-2208 moves from 13 Nov to 27 Nov
Step 3: Allocate existing Pune material
Plain Text
MO-0876 requires 400 MCU
Existing Pune inventory: 400
MO-0876 receives allocation
Remaining projected available MCU: 0
Step 4: Detect shortage
Plain Text
MO-0882 and MO-0889 cannot obtain required MCU
until delayed PO-2208 arrives
Step 5: Reschedule production

Use:

100-unit batches
200 MCU per batch
100 finished units per day
Stable priority queue
Step 6: Calculate customer fulfilment
Plain Text
CO-0701 remains on time
CO-0704 becomes late
CO-0711 becomes late
Step 7: Calculate exposure
Plain Text
Breached customer orders: 2
Late revenue:
₹800,000 + ₹800,000
= ₹1,600,000
Step 8: Produce causal traces

Each late order must trace through:

Plain Text
outage
→ PO-2208
→ CMP-MCU-42 shortage
→ manufacturing order
→ customer order
→ SLA breach
→ revenue at risk
Golden acceptance requirement

All fields must match the Phase 4 frozen expected result:

Exact timestamps
Exact quantities
Exact delay hours
Exact breach counts
Exact revenue
Exact causal parents
Exact rule IDs
Exact attribution classes
Golden-first rule

Do not special-case golden identifiers in implementation.

Prohibited:

Python
if scenario_id == "SCN-GOLD-001":
return expected_result

The golden scenario must pass through the same engine used for every benchmark case.

Deliverables
Plain Text
tests/impact/golden/
artifacts/phase-5/golden-impact-result.json
artifacts/phase-5/golden-comparison-report.md

23. Phase 5S: Benchmark and Correctness Evaluation
Goal

Measure engine correctness against the frozen Phase 4 ground truth.

Evaluation partitions
Development

Visible during implementation.

Validation

Used to tune implementation details without changing business rules.

Test

Frozen and evaluated only after the engine is ready.

Adversarial

Used to verify correct failure behavior.

Correctness metrics
Affected-entity precision
Precision=CorrectlyPredictedAffectedEntitiesAllPredictedAffectedEntitiesPrecision = \frac{CorrectlyPredictedAffectedEntities} {AllPredictedAffectedEntities}Precision=AllPredictedAffectedEntitiesCorrectlyPredictedAffectedEntities​
Affected-entity recall
Recall=CorrectlyPredictedAffectedEntitiesAllGroundTruthAffectedEntitiesRecall = \frac{CorrectlyPredictedAffectedEntities} {AllGroundTruthAffectedEntities}Recall=AllGroundTruthAffectedEntitiesCorrectlyPredictedAffectedEntities​

Calculate independently for:

Purchase orders
Components
Production orders
Customer orders
Numerical exact-match rate
ExactMatch=NumericalFieldsMatchingGroundTruthAllEvaluatedNumericalFieldsExactMatch = \frac{NumericalFieldsMatchingGroundTruth} {AllEvaluatedNumericalFields}ExactMatch=AllEvaluatedNumericalFieldsNumericalFieldsMatchingGroundTruth​

For deterministic monetary and quantity outputs:

Plain Text
Target: 100%
Timestamp accuracy

For exact deterministic scenarios:

Plain Text
Target: Exact timestamp match

Do not hide boundary errors behind wide tolerances.

SLA classification accuracy
SLAAccuracy=CorrectSLAClassificationsAllEvaluatedOrderLinesSLAAccuracy = \frac{CorrectSLAClassifications} {AllEvaluatedOrderLines}SLAAccuracy=AllEvaluatedOrderLinesCorrectSLAClassifications​

Target:

Plain Text
100% for supported, complete-data scenarios
Revenue-at-risk fidelity
FinancialFidelity=CorrectRevenueAtRiskValuesAllScenariosWithDefinedGroundTruthFinancialFidelity = \frac{CorrectRevenueAtRiskValues} {AllScenariosWithDefinedGroundTruth}FinancialFidelity=AllScenariosWithDefinedGroundTruthCorrectRevenueAtRiskValues​

Target:

Plain Text
100%
Causal-trace edge precision
CausalPrecision=CorrectPredictedCausalEdgesAllPredictedCausalEdgesCausalPrecision = \frac{CorrectPredictedCausalEdges} {AllPredictedCausalEdges}CausalPrecision=AllPredictedCausalEdgesCorrectPredictedCausalEdges​
Causal-trace edge recall
CausalRecall=CorrectPredictedCausalEdgesAllExpectedCausalEdgesCausalRecall = \frac{CorrectPredictedCausalEdges} {AllExpectedCausalEdges}CausalRecall=AllExpectedCausalEdgesCorrectPredictedCausalEdges​

Targets:

Plain Text
Golden: 100% precision and recall
Supported test scenarios: ≥98%

If the ground truth permits equivalent causal representations, normalize paths before comparison.

Data-quality classification accuracy

Target:

Plain Text
100%

for:

Complete
Partial
Insufficient data
Invalid input
Required target table
Metric	Golden	Test suite
Affected PO precision	100%	≥99%
Affected PO recall	100%	≥99%
Component precision	100%	≥99%
Component recall	100%	≥99%
Production-order precision	100%	≥98%
Production-order recall	100%	≥98%
Customer-order precision	100%	≥98%
Customer-order recall	100%	≥98%
SLA classification	100%	100%
Quantity fidelity	100%	100%
Financial fidelity	100%	100%
Feasible complete-data run completion	100%	100%
Data-quality classification	100%	100%

For a deterministic engine, unexplained financial or quantity mismatches should block release rather than be accepted as approximate accuracy.

Deliverables
Plain Text
benchmarks/impact/
artifacts/phase-5/impact-benchmark-results.json
artifacts/phase-5/impact-benchmark-report.md
24. Phase 5T: Performance and Scalability Evaluation
Goal

Ensure the engine is fast enough for an interactive judge demonstration.

Test scales
Plain Text
tiny
demo
standard
stress
Performance measurements

Measure separately:

State reconstruction
Disruption resolution
Inventory projection
Material allocation
Production scheduling
Customer fulfilment
Financial calculation
Causal trace construction
Persistence
Total runtime
Initial targets
Operation	Demo p95	Standard p95
State reconstruction	<500 ms	<1.5 s
Disruption resolution	<100 ms	<300 ms
Inventory projection	<500 ms	<1.5 s
Production scheduling	<1 s	<3 s
Customer/SLA impact	<300 ms	<1 s
Causal trace build	<300 ms	<1 s
Full do-nothing calculation	<2 s	<6 s

The demo target is stricter than the standard benchmark because the judge-facing experience must feel immediate.

Reporting requirements

Every benchmark report must include:

Hardware
CPU
Memory
Operating system
Python version
Db2 version
Dataset version
Rule-set version
Warm or cold run
Scenario counts
Median
p95
Maximum
Error rate
Memory target

The standard dataset engine should operate within a documented memory envelope, initially:

Plain Text
Target peak application memory: <1.5 GB

If higher, document why and optimize state loading.

Performance principles

Prioritize:

Correctness
Determinism
Explainability
Performance

Do not remove intermediate evidence merely to improve latency.

Deliverables
Plain Text
artifacts/phase-5/performance/
├── demo-performance.json
├── standard-performance.json
├── stress-performance.json
└── performance-report.md
25. Phase 5U: Testing and Adversarial Validation
Goal

Prove correctness, safety, and predictable failure behavior.

25.1 Unit tests

Test:

Outstanding quantity
Disrupted arrival
Inventory delta
BOM requirement
Batch requirement
Material-ready time
Capacity-ready time
Projected start
Projected completion
Late quantity
Delay hours
Revenue at risk
Stable tie-breaking
Canonical result hashing
25.2 Property-based tests

Useful invariants:

Inventory conservation
Ending=Opening+In−OutEnding = Opening + In - OutEnding=Opening+In−Out
Allocation bound
Allocated≤EligibleAvailableAllocated \le EligibleAvailableAllocated≤EligibleAvailable
Production bound
Completed≤PlannedCompleted \le PlannedCompleted≤Planned
Customer fulfilment bound
OnTime+Late≤OpenQuantityOnTime + Late \le OpenQuantityOnTime+Late≤OpenQuantity
Revenue bound
0≤RevenueAtRisk≤OpenRevenue0 \le RevenueAtRisk \le OpenRevenue0≤RevenueAtRisk≤OpenRevenue
Time ordering
Completion≥StartCompletion \ge StartCompletion≥Start Delivery≥ProductAvailabilityDelivery \ge ProductAvailabilityDelivery≥ProductAvailability
Disruption monotonicity under controlled conditions

If all other inputs remain fixed and a receipt is delayed further, the engine must not calculate earlier component availability.

This does not mean every customer outcome must become worse because unused inventory may absorb the delay.

25.3 Integration tests

Test:

State reconstruction from Db2
Impact run persistence
Golden scenario
Historical replay
Restart and rerun
Failed persistence
Idempotent request
Rule-version selection
25.4 Adversarial tests
Unknown supplier

Expected:

Plain Text
REJECTED
UNKNOWN_SUPPLIER
Negative duration

Expected:

Plain Text
REJECTED
INVALID_DISRUPTION_INTERVAL
Missing inventory state

Expected:

Plain Text
PARTIALLY_COMPLETED or REJECTED
MISSING_CRITICAL_DATA

depending on scope.

Missing BOM

Affected production calculation:

Plain Text
INSUFFICIENT_DATA
Duplicate inventory event

Expected:

Detected by event identity
Not counted twice
Overlapping BOM versions

Expected:

Plain Text
INVALID_OPERATIONAL_STATE
Purchase order fully received

Expected:

Not affected by the future outage
Partial receipt

Expected:

Only outstanding quantity is delayed
No-impact outage

Expected:

Plain Text
0 operational shortages
0 new SLA breaches
₹0 disruption-caused revenue at risk
Pre-existing late order

Expected attribution:

Plain Text
PRE_EXISTING

not DISRUPTION_CAUSED.

Horizon shortage

Expected:

Plain Text
NOT_COMPLETED_WITHIN_HORIZON

No fabricated completion date.

Concurrent identical requests

Expected:

One stable business result
No inconsistent duplicates
Test targets
Plain Text
Critical path test pass rate: 100%
Golden test pass rate: 100%
Supported benchmark numerical fidelity: 100%
Flaky tests: 0
Severity-1 defects: 0
Deliverables
Plain Text
tests/impact/
├── unit/
├── property/
├── integration/
├── golden/
├── benchmark/
├── temporal/
└── adversarial/
26. Phase 5V: Observability and Diagnostics
Goal

Make failures diagnosable without leaking secrets or overwhelming users.

Structured logs

Each log entry should include:

Plain Text
correlation_id
impact_run_id
scenario_id
phase
entity_type
entity_id
rule_id
status
duration_ms
error_code
Pipeline-stage timings

Capture:

Plain Text
state_reconstruction_ms
disruption_resolution_ms
inventory_projection_ms
material_allocation_ms
production_scheduling_ms
customer_impact_ms
provenance_build_ms
persistence_ms
total_ms
Diagnostic counters
Records loaded
Purchase orders affected
Receipt events changed
Inventory timelines processed
Shortages found
Production batches scheduled
Customer lines calculated
Causal nodes generated
Warnings
Errors
Safe logging

Never log:

Passwords
Db2 connection strings with credentials
LLM keys
Entire unrestricted document content
Unnecessary raw personal data

The dataset is synthetic, but secure behavior should still be implemented.

Debug trace mode

Provide an optional development mode that emits per-rule calculations.

Production or demo default should preserve calculation traces in structured persistence without flooding standard logs.

Deliverables
Plain Text
src/backend/chronosdb/observability/
docs/impact-engine/observability.md
27. Phase 5W: Independent Review and Release Gate
Goal

Review the engine as both a domain system and a judging artifact.

Domain review

Check:

Outage affects only eligible supply.
Already received material is preserved.
Inventory does not appear or disappear.
Material allocation obeys priority.
Production capacity is respected.
Customer orders receive correct output quantities.
Revenue at risk uses late quantity only.
Temporal review

Check:

State is reconstructed correctly.
Late-arriving data is excluded.
Effective records are selected correctly.
Timestamp boundaries are consistent.
Replay is stable.
Software review

Check:

Domain logic is separated from persistence.
Functions have narrow responsibility.
Rule versions are explicit.
Decimal arithmetic is used.
Stable ordering is enforced.
Errors are typed.
Intermediate results are inspectable.
Audit review

Check:

Every headline metric has provenance.
Every customer breach has a causal path.
Result hash is stable.
Failed runs remain diagnosable.
Operational records remain unchanged.
Judge review

Check:

The engine shows more than a spreadsheet calculation.
Cascading impact is easy to explain.
Db2 operational records are visibly central.
The result is credible without an LLM.
A reviewer can inspect why each order became late.
Required signoffs
Plain Text
Domain logic
Temporal correctness
Financial correctness
Software quality
Benchmark correctness
Auditability
Demo readiness
Deliverables
Plain Text
docs/impact-engine/review-signoff.md
docs/impact-engine/phase-5-completion-report.md
28. Phase 5 Quality Benchmarks
28.1 Deterministic-result stability
DRS=RunsMatchingExpectedResultHashAllRepeatedRunsDRS = \frac{RunsMatchingExpectedResultHash} {AllRepeatedRuns}DRS=AllRepeatedRunsRunsMatchingExpectedResultHash​

Target:

Plain Text
100%
28.2 Numerical fidelity
NF=NumericalOutputsMatchingGroundTruthAllEvaluatedNumericalOutputsNF = \frac{NumericalOutputsMatchingGroundTruth} {AllEvaluatedNumericalOutputs}NF=AllEvaluatedNumericalOutputsNumericalOutputsMatchingGroundTruth​

Target:

Plain Text
100%
28.3 Causal coverage
CC=KeyImpactOutputsWithCompleteCausalTraceAllKeyImpactOutputsCC = \frac{KeyImpactOutputsWithCompleteCausalTrace} {AllKeyImpactOutputs}CC=AllKeyImpactOutputsKeyImpactOutputsWithCompleteCausalTrace​

Target:

Plain Text
100%
28.4 Provenance coverage
PC=KeyOutputsWithCompleteProvenanceAllKeyOutputsPC = \frac{KeyOutputsWithCompleteProvenance} {AllKeyOutputs}PC=AllKeyOutputsKeyOutputsWithCompleteProvenance​

Target:

Plain Text
100%
28.5 State reconstruction accuracy
SRA=ReconstructedStatesMatchingFrozenStateAllHistoricalStateFixturesSRA = \frac{ReconstructedStatesMatchingFrozenState} {AllHistoricalStateFixtures}SRA=AllHistoricalStateFixturesReconstructedStatesMatchingFrozenState​

Target:

Plain Text
100%
28.6 Impact entity F1
F1=2×Precision×RecallPrecision+RecallF1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}F1=2×Precision+RecallPrecision×Recall​

Target:

Plain Text
Golden: 1.0
Supported test scenarios: ≥0.98
28.7 Failure-classification accuracy
FCA=CorrectErrorOrQualityClassificationsAllFailureFixturesFCA = \frac{CorrectErrorOrQualityClassifications} {AllFailureFixtures}FCA=AllFailureFixturesCorrectErrorOrQualityClassifications​

Target:

Plain Text
100%
28.8 Demo latency

Target:

Plain Text
Demo scenario p95 end-to-end impact calculation: <2 seconds
29. Phase 5 Scorecard
Category	Weight
Input and state correctness	10
Disruption and supply projection	10
Inventory calculation	13
Material allocation	10
Production scheduling	13
Customer and SLA calculation	10
Financial fidelity	8
Causality and provenance	10
Determinism and replay	6
Testing and failure handling	6
Performance and observability	4
Total	100
Passing threshold
Plain Text
95–100: Pass
90–94: Conditional pass
Below 90: Fail
Automatic failures

Phase 5 fails regardless of score if:

The engine uses an LLM for numerical business calculations.
Golden headline values do not match ground truth.
Inventory conservation fails.
Material is allocated twice.
Facility capacity is exceeded.
A receipt is consumed before arrival.
Revenue at risk includes on-time quantity.
Missing values are treated as zero.
Pre-existing lateness is attributed to the disruption.
Identical inputs produce different business outputs.
Operational records are modified by the calculation.
A breached customer order lacks a causal path.
Expected benchmark results are accessed at runtime.
Test-specific identifiers are hardcoded.
Completed runs cannot be replayed.
Rule version is absent from the result.
Critical errors are hidden behind a successful status.
30. Required Phase 5 Repository Structure
Plain Text
src/backend/chronosdb/impact/
├── __init__.py
├── contracts/
│ ├── requests.py
│ ├── results.py
│ ├── errors.py
│ └── enums.py
├── rules/
│ ├── registry.py
│ ├── loader.py
│ └── versions.py
├── state/
│ ├── reconstruction.py
│ ├── canonicalization.py
│ ├── hashing.py
│ └── validation.py
├── disruption/
│ ├── validation.py
│ ├── scope.py
│ └── supplier_outage.py
├── supply/
│ ├── outstanding.py
│ ├── receipts.py
│ └── projection.py
├── inventory/
│ ├── events.py
│ ├── timeline.py
│ ├── allocation.py
│ ├── shortage.py
│ └── reconciliation.py
├── materials/
│ ├── bom.py
│ ├── requirements.py
│ └── allocation.py
├── production/
│ ├── batches.py
│ ├── capacity.py
│ ├── priority.py
│ └── scheduler.py
├── fulfilment/
│ ├── product_availability.py
│ ├── allocation.py
│ ├── delivery.py
│ └── sla.py
├── financial/
│ ├── revenue.py
│ ├── delay.py
│ └── metrics.py
├── causality/
│ ├── nodes.py
│ ├── edges.py
│ ├── builder.py
│ └── attribution.py
├── provenance/
│ ├── calculation_trace.py
│ ├── evidence.py
│ └── serializer.py
├── validation/
│ ├── input.py
│ ├── data_quality.py
│ └── invariants.py
├── persistence/
│ ├── repository.py
│ ├── run_store.py
│ └── result_store.py
└── orchestration/
├── pipeline.py
├── stages.py
└── service.py
 
config/rules/
└── impact-rules-v1.0.0.yaml
 
schemas/
├── impact-request.schema.json
├── impact-result.schema.json
└── causal-trace.schema.json
 
tests/impact/
├── unit/
├── property/
├── integration/
├── temporal/
├── golden/
├── benchmark/
└── adversarial/
 
benchmarks/impact/
├── run_impact_benchmark.py
├── compare_ground_truth.py
└── benchmark_config.yaml
 
docs/impact-engine/
├── phase-4-handoff-review.md
├── engine-contract.md
├── input-contract.md
├── output-contract.md
├── rule-catalogue.md
├── state-reconstruction.md
├── disruption-resolution.md
├── inbound-supply-projection.md
├── inventory-timeline.md
├── material-allocation.md
├── shortage-calculation.md
├── production-scheduling.md
├── customer-fulfilment.md
├── sla-and-financial-impact.md
├── causality-and-provenance.md
├── data-quality-and-partial-results.md
├── determinism-contract.md
├── execution-ledger.md
├── observability.md
├── review-signoff.md
├── phase-5-traceability-matrix.csv
└── phase-5-completion-report.md
 
artifacts/phase-5/
├── golden-impact-result.json
├── golden-comparison-report.md
├── impact-benchmark-results.json
├── impact-benchmark-report.md
├── determinism-report.json
└── performance/
31. Phase 5 Traceability Matrix

Create:

Plain Text
docs/impact-engine/phase-5-traceability-matrix.csv

Recommended columns:

Plain Text
phase1_requirement_id
phase2_rule_id
phase4_source_file
engine_module
function_or_service
rule_id
input_fields
output_fields
unit_test_ids
integration_test_ids
benchmark_scenario_ids
golden_evidence
status
notes

Example:

Plain Text
FR-IMP-012,
FIN-RAR-001,
demand/customer_order_lines.csv,
financial/revenue.py,
calculate_revenue_at_risk,
FIN-004,
late_quantity|unit_revenue,
revenue_at_risk,
UT-FIN-004,
IT-GOLD-001,
SCN-GOLD-001|SCN-0014,
golden/expected_do_nothing.json,
APPROVED,
Late quantity only
32. Phase 5 Execution Order

Execute Phase 5 in this order. Do not start broad benchmark tuning before the golden scenario passes at every intermediate stage.

Work Block 1: Intake and contracts
Plain Text
5A. Verify dataset and ground-truth checksums
5A. Validate golden input state
5B. Freeze engine boundaries
5C. Implement typed input and output models
5D. Implement rule registry
Work Block 2: State reconstruction
Plain Text
5E. Load active master records
5E. Reconstruct inventory
5E. Reconstruct open purchase orders
5E. Reconstruct production state
5E. Reconstruct customer state
5E. Generate state hash
5E. Pass temporal replay fixtures
Work Block 3: Supply impact
Plain Text
5F. Validate supplier outage
5F. Resolve disruption scope
5F. Select affected purchase orders
5F. Compute outstanding quantities
5F. Apply outage and recovery lag
5G. Generate projected receipt events
Work Block 4: Inventory and materials
Plain Text
5H. Implement event-driven inventory timeline
5H. Implement event ordering
5I. Implement BOM explosion
5I. Implement batch material requirements
5I. Implement allocation priority
5J. Implement shortage detection
5J. Emit shortage evidence
Work Block 5: Production
Plain Text
5K. Build production batches
5K. Implement facility capacity calendar
5K. Implement material-ready time
5K. Implement capacity-ready time
5K. Implement stable scheduling
5K. Emit production impact
Work Block 6: Customer and finance
Plain Text
5L. Generate product-availability events
5L. Allocate product to customer lines
5L. Calculate projected delivery
5M. Classify SLA status
5M. Calculate late quantity
5M. Calculate revenue at risk
5M. Calculate delay metrics
Work Block 7: Causality and quality
Plain Text
5N. Generate causal nodes
5N. Generate causal edges
5N. Assign disruption attribution
5N. Build calculation provenance
5O. Implement partial-result handling
5O. Implement typed errors and warnings
Work Block 8: Determinism and persistence
Plain Text
5P. Generate request fingerprints
5P. Implement result canonicalization
5P. Implement result hashing
5Q. Persist runs and intermediate results
5Q. Enforce immutable completed output
Work Block 9: Golden scenario
Plain Text
5R. Run state comparison
5R. Run supply comparison
5R. Run inventory comparison
5R. Run production comparison
5R. Run customer comparison
5R. Run financial comparison
5R. Run causal comparison
5R. Resolve every mismatch
5R. Freeze golden engine output
Work Block 10: Benchmark and optimization
Plain Text
5S. Run development scenarios
5S. Run validation scenarios
5U. Run adversarial fixtures
5T. Profile execution stages
5T. Optimize without changing semantics
5S. Run frozen test partition
Work Block 11: Review and release
Plain Text
5V. Validate observability
5W. Conduct domain review
5W. Conduct financial review
5W. Conduct temporal review
5W. Conduct code review
5W. Calculate Phase 5 score
5W. Write completion report
5X. Prepare Phase 6 handoff
33. Phase 5 Final Gate Checklist
Inputs and contracts
 Dataset version is pinned.
 Dataset checksums match.
 Rule-set version is pinned.
 Request schema is complete.
 Result schema is complete.
 Runtime cannot access expected benchmark answers.
 No LLM dependency exists.
State reconstruction
 Effective master records are selected correctly.
 Information-time rules are enforced.
 Inventory reconstructs exactly.
 Outstanding purchase orders reconstruct exactly.
 Production state reconstructs exactly.
 Customer state reconstructs exactly.
 State hash matches the frozen golden state.
 Future information leakage is zero.
Disruption and supply
 Disruption interval validates.
 Scope resolves correctly.
 Fully received orders are excluded.
 Partially received orders use outstanding quantity.
 Cancelled orders are excluded.
 Recovery lag is applied exactly once.
 Original and disrupted receipts are preserved.
 Out-of-horizon receipts are handled correctly.
Inventory and materials
 Inventory events have stable ordering.
 Opening balance reconciles.
 Receipt events apply at the correct time.
 BOM selection is correct.
 Batch requirements are correct.
 Reservations are not double counted.
 Materials are not double allocated.
 Shortage timestamps are exact.
 Shortage quantities are exact.
 Physical inventory is conserved.
Production
 Batch creation is correct.
 Material-ready time is correct.
 Capacity-ready time is correct.
 Priority sorting is stable.
 Capacity is never exceeded.
 Material is consumed once.
 Projected starts are correct.
 Projected completions are correct.
 Horizon failures are explicit.
Customer and finance
 Product availability is calculated correctly.
 Customer priority is applied correctly.
 Fulfilment segments reconcile.
 Delivery lead time is applied correctly.
 SLA classification is correct.
 Partial late quantity is handled.
 Revenue at risk uses late quantity only.
 Currency remains INR.
 Revenue totals reconcile.
 Delay metrics use documented units.
Causality and provenance
 Every affected order has a causal trace.
 Every headline number has provenance.
 Pre-existing impact is distinguished.
 Disruption-caused impact is identified.
 Causal edges reference valid entities.
 Rule IDs are present.
 Input-state hash is present.
 Result hash is present.
Data quality
 Missing and zero are distinct.
 Critical missing data blocks affected calculations.
 Unaffected calculations continue safely.
 Partial runs are labelled.
 Errors are machine-readable.
 Warnings are preserved.
 Successful status never hides critical failure.
Determinism and persistence
 Golden result is stable across 100 runs.
 Benchmark sample is stable across repeated runs.
 Cross-process result is stable.
 Database restart does not change result.
 Idempotency works.
 Duplicate requests do not create inconsistent results.
 Completed output is immutable.
 Operational records remain unchanged.
Correctness and testing
 Golden output matches ground truth exactly.
 Development benchmark passes.
 Validation benchmark passes.
 Frozen test benchmark meets targets.
 Numerical fidelity is 100%.
 SLA classification is 100%.
 Failure classification is 100%.
 Property tests pass.
 Adversarial tests pass.
 Flaky tests are zero.
 Severity-1 defects are zero.
Performance
 Demo p95 is below two seconds.
 Standard p95 is below six seconds.
 Stage timings are recorded.
 Peak memory is measured.
 Performance hardware is documented.
 Correctness was not weakened for speed.
Release
 Traceability matrix is complete.
 Benchmark report is complete.
 Determinism report is complete.
 Performance report is complete.
 Independent review is signed off.
 Phase 5 score is at least 95.
 No automatic-failure condition remains.
34. Phase 5X: Phase 6 Handoff
Next phase
Phase 6: Counterfactual Simulation Engine
Phase 6 goal

Reuse the deterministic Phase 5 core while applying isolated intervention overlays:

Warehouse transfer
Purchase-order expedition
Alternate supplier
Production rescheduling
Hybrid recovery plan

Phase 6 must calculate each intervention against the same disrupted state without mutating the operational baseline.

Mandatory Phase 6 inputs
Impact engine
State reconstruction
Supply projection
Inventory timeline
Material allocation
Production scheduler
Customer fulfilment
SLA calculation
Financial calculation
Causality
Provenance
Frozen contracts
Rule-set version
Input-state hashing
Result hashing
Error model
Data-quality model
Persistence model
Baseline output

The Phase 5 do-nothing result becomes the comparison reference for every Phase 6 candidate.

Required Phase 6 identity

For each candidate:

Plain Text
same operational state
same disruption
same horizon
same rule set
same allocation policy
same scheduling policy
different intervention overlay
Required Phase 6 calculations
RevenueProtectedi=RevenueAtRiskDoNothing−RevenueAtRiskiRevenueProtected_i = RevenueAtRisk_{DoNothing} - RevenueAtRisk_iRevenueProtectedi​=RevenueAtRiskDoNothing​−RevenueAtRiski​ BreachesAvoidedi=BreachesDoNothing−BreachesiBreachesAvoided_i = Breaches_{DoNothing} - Breaches_iBreachesAvoidedi​=BreachesDoNothing​−Breachesi​ DelayReductioni=DelayDoNothing−DelayiDelayReduction_i = Delay_{DoNothing} - Delay_iDelayReductioni​=DelayDoNothing​−Delayi​
Phase 5 handoff package
Plain Text
artifacts/phase-5-handoff/
├── impact-engine-contract.json
├── rule-set-manifest.json
├── golden-impact-result.json
├── benchmark-summary.json
├── determinism-report.json
├── performance-report.json
├── error-catalogue.json
├── causal-trace-schema.json
└── phase-5-completion-report.md
Final Phase 5 Outcome

When Phase 5 passes, ChronosDB will have a trustworthy computational foundation:

A supplier outage alters only eligible future supply.
The changed supply produces a precise inventory timeline.
Inventory shortages block exact production batches.
Material and capacity jointly determine production timing.
Production timing determines customer fulfilment.
Customer lateness produces proportional revenue at risk.
Pre-existing and disruption-caused impacts remain separate.
Every number has a rule, source record, state hash, and causal path.
Repeated executions produce the same result.
The entire workflow works without an LLM.

The locked deliverable from this phase is:

chronosdb-impact-engine-v1.0.0

The next phase is:

Phase 6: Counterfactual Simulation Engine

Apply isolated recovery interventions and calculate how each one changes the deterministic do-nothing outcome.