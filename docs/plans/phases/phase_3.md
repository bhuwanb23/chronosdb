Phase 3 Deep Dive: Dataset Engineering and Ground-Truth Construction

Phase 2 established the formal supply-chain world ChronosDB must model. Phase 3 now turns those rules into a realistic, deterministic, versioned, and benchmark-ready synthetic dataset.

This phase is not simply “generate some CSV files.” It must produce a dataset whose operational records, historical events, disruption scenarios, evidence documents, and expected outputs are all internally consistent. If Phase 3 is weak, later accuracy claims will be meaningless because the simulator will be evaluated against unreliable ground truth.

1. Phase Definition
Phase name

Dataset Engineering and Ground-Truth Construction

Primary goal

Build a reproducible synthetic supply-chain dataset and frozen evaluation suite that:

Conforms to every Phase 2 domain rule.
Supports the locked supplier-outage scenario.
Exercises normal, edge, failure, and adversarial conditions.
Produces independently verifiable expected outcomes.
Can be seeded into IBM Db2 repeatedly.
Supports structured queries and later vector retrieval.
Enables fair comparison between ChronosDB and benchmark baselines.
Contains no private, copyrighted, or real customer information.
Required result

At the end of Phase 3, we must have:

A versioned dataset specification
A deterministic synthetic-data generator
Referentially valid operational data
Historical snapshots and events
Evidence documents for later Db2 vector retrieval
A corrected and frozen golden scenario
A benchmark scenario catalogue
Machine-readable expected outcomes
Negative and adversarial test fixtures
Dataset-quality reports
Dataset cards and limitations
Reproduction commands
Dataset checksums
A clean handoff to Phase 4
2. Phase 3 Definition of Done

Phase 3 passes only when:

A clean environment can generate the same dataset from the same configuration and random seed, validate every domain invariant, execute ground-truth calculations for all frozen benchmark scenarios, reproduce the approved golden results, and emit versioned files ready for loading into IBM Db2.

Phase 4 must not need to invent data semantics or manually repair generated records.

3. Phase 3 Boundaries
In scope
Synthetic enterprise definition
Dataset scale
Distribution design
Identifier conventions
Deterministic generation
Operational master data
Transactional data
Historical snapshots
Disruption events
Intervention parameters
Evidence documents
Golden scenario data
Benchmark scenarios
Ground-truth calculations
Data validation
Dataset statistics
Privacy and licensing controls
Data versioning
Reproducibility
Export formats
Phase 4 load contract
Out of scope
Final Db2 physical schema
Db2 indexes
Production SQL migrations
Simulation-engine implementation
Optimization implementation
Embedding generation
Vector-index construction
Application API
User interface
LLM prompts
Live external datasets
Real ERP integration
4. Phase 3 Structure
Plain Text
Phase 3
├── 3A. Phase 2 handoff validation
├── 3B. Dataset objectives and benchmark contract
├── 3C. Synthetic enterprise blueprint
├── 3D. Dataset scale and distribution design
├── 3E. Identifier, serialization and versioning standards
├── 3F. Deterministic generation architecture
├── 3G. Master-data generation
├── 3H. Operational and transactional-data generation
├── 3I. Historical and temporal-data construction
├── 3J. Disruption and intervention-data generation
├── 3K. Evidence-document corpus
├── 3L. Golden-scenario correction and freezing
├── 3M. Benchmark scenario suite
├── 3N. Ground-truth oracle
├── 3O. Negative, boundary and adversarial fixtures
├── 3P. Data validation and invariant enforcement
├── 3Q. Statistical and realism assessment
├── 3R. Privacy, licensing and contamination controls
├── 3S. Dataset packaging and reproducibility
├── 3T. Dataset benchmark and quality score
├── 3U. Independent review and release freeze
└── 3V. Phase 4 handoff
5. Phase 3A: Phase 2 Handoff Validation
Goal

Confirm that the dataset will implement the approved domain model exactly.

Required Phase 2 inputs

Verify:

Domain glossary
Conceptual entity model
Relationship model
State transitions
Unit and financial model
Temporal model
Supplier-outage model
Inventory and allocation model
BOM rules
Production scheduling rules
Customer fulfilment rules
SLA and revenue rules
Intervention model
Counterfactual model
Formula catalogue
Provenance model
Data-quality model
Domain invariants
Golden-scenario specification
Domain tests
Traceability matrix
Handoff questions

Before generation begins, resolve:

Is partial production allowed?
Is partial customer delivery allowed?
What production granularity is used?
Does facility capacity apply across products or per product?
When are BOM materials consumed?
Which inventory level protects transfer feasibility?
How are customer lines allocated to production?
What counts as outstanding purchase-order quantity?
Which costs are incremental?
How are ties resolved?
Locked recommendation

For the Phase 3 MVP:

Plain Text
Partial production: Allowed in 100-unit batches
Partial customer delivery: Allowed
Production capacity: Shared facility capacity
Material consumption: At batch start
Customer allocation: Priority, promised date, order ID
Time resolution: One hour
Planning calculations: Calendar time
Primary currency: INR
Component unit: EA for golden scenario

If Phase 2 locked different rules, Phase 2 remains authoritative and the difference must be recorded.

Deliverable
Plain Text
docs/data/phase-2-handoff-review.md
Exit gate
Every generated field has a Phase 2 meaning.
Every ground-truth output has a frozen formula.
No Priority 0 domain question remains open.
Golden-scenario assumptions are internally consistent.
Data-generation rules do not silently redefine business behavior.
6. Phase 3B: Dataset Objectives and Benchmark Contract
Goal

Define which questions the dataset must support before generating records.

Primary analytical questions

The dataset must support:

Which supply commitments are affected by an outage?
Which components become unavailable?
When and where does inventory become insufficient?
Which production orders are delayed?
Which customer orders become late?
How much revenue becomes at risk?
Which interventions are feasible?
Which intervention best satisfies a chosen objective?
Which historical incidents and procedures are relevant?
Can every result be traced to the underlying records?
Dataset layers
Layer 1: Operational truth
Suppliers
Components
Products
BOMs
Warehouses
Facilities
Agreements
Inventory
Purchase orders
Production orders
Customer orders
Layer 2: Historical state
Inventory snapshots
Status changes
Deliveries
Consumption events
Supplier performance
Past disruption events
Layer 3: Scenario inputs
Outages
Budgets
Objectives
Constraints
As-of times
Simulation horizons
Layer 4: Evidence documents
Supplier notices
Standard operating procedures
Incident reports
SLA policies
Alternate-supplier approvals
Layer 5: Ground truth
Expected affected entities
Expected shortage
Expected delays
Expected breaches
Expected costs
Expected feasibility
Expected recommendations
Expected causal traces
Required dataset partitions
Plain Text
development
validation
test
golden
adversarial
Development

Used while implementing and debugging.

Validation

Used for tuning deterministic parameters and retrieval configuration.

Test

Frozen before tuning concludes and used for final evaluation.

Golden

Small, manually validated scenarios for exact correctness.

Adversarial

Malformed, contradictory, extreme, or unsafe cases.

Leakage rule

The final test expected outcomes must not be used to tune threshold values or manually special-case implementation behavior.

Deliverable
Plain Text
docs/data/dataset-and-benchmark-contract.md
7. Phase 3C: Synthetic Enterprise Blueprint
Goal

Create a coherent fictional manufacturer rather than disconnected random tables.

Enterprise identity

Use a clearly synthetic organization:

Plain Text
Company:
Asterion Control Systems
 
Industry:
Industrial electronics manufacturing
 
Primary products:
Industrial controllers and monitoring units
 
Primary regions:
India
 
Planning currency:
INR
 
Planning timezone:
Asia/Kolkata
 
Canonical timestamp storage:
UTC

Add this disclaimer everywhere required:

Asterion Control Systems and all suppliers, customers, transactions, incidents, prices, and operational records in this repository are synthetic and created solely for demonstration and evaluation.

Operational network
Facilities
Plain Text
FAC-PUNE
FAC-CHENNAI
Warehouses
Plain Text
WH-PUNE
WH-CHENNAI
WH-GURUGRAM
Supplier regions
India
Southeast Asia
East Asia
Europe

Regional diversity should affect lead time, not introduce unsupported geopolitical inference.

Product families

Recommended:

Plain Text
Controller-X
Controller-Pro
Sensor-Hub
Gateway-Edge
Monitor-Lite
Component families
Microcontrollers
Memory modules
Power units
Sensors
Connectors
Printed circuit boards
Casings
Cables
Displays
Communication modules
Customer classes
Plain Text
STRATEGIC
ENTERPRISE
STANDARD

Possible SLA patterns:

Class	Expected treatment
Strategic	Highest allocation priority
Enterprise	Medium priority
Standard	Standard priority

Do not use real customer names.

Deliverables
Plain Text
docs/data/synthetic-enterprise-blueprint.md
config/enterprise.yaml
8. Phase 3D: Dataset Scale and Distribution Design
Goal

Choose a scale large enough to demonstrate enterprise-like relationships while remaining reproducible and inspectable.

Recommended MVP scale
Entity	Target
Suppliers	24
Supplier-component agreements	120–180
Components	80
Products	16
BOM versions	24–32
BOM lines	160–240
Warehouses	3
Facilities	2
Inventory snapshot rows	12,000–18,000
Purchase orders	600
Production orders	400
Customers	80
Customer orders	1,000
Customer-order lines	1,300–1,800
Disruption events	100
Historical incident reports	60
Operating procedures and policies	25–40
Frozen benchmark scenarios	60
Adversarial fixtures	25–40
Historical period

Recommended generation window:

Plain Text
180 days of history
+
30-day future planning horizon
Inventory snapshot frequency

Recommended default:

Plain Text
Daily snapshots at 00:00 UTC

For the golden scenario and selected benchmarks:

Plain Text
Hourly event-level changes

This balances scale and temporal precision.

Distribution targets
Supplier concentration

Model a realistic dependency mix:

15% of components: single approved supplier
45%: two approved suppliers
30%: three approved suppliers
10%: four or more approved suppliers
Criticality
Critical: 20%
High: 30%
Medium: 35%
Low: 15%
Lead time

Suggested synthetic ranges:

Supplier region	Lead time
Same region	2–5 days
Other Indian region	4–8 days
Southeast/East Asia	8–20 days
Europe	12–25 days

Use configurable distributions rather than hardcoded record-by-record choices.

Product demand

Use a right-skewed distribution:

A small number of high-demand products
Several medium-demand products
Rare low-demand products

A log-normal or gamma distribution is more suitable than a uniform distribution.

Order priority
High: 15%
Medium: 50%
Normal: 35%
Disruption severity
Minor delay: 35%
Partial outage: 30%
Full supplier outage: 25%
Multi-factor or edge case: 10%
Scale tiers

Support at least:

Plain Text
tiny
standard
stress
Tiny

For local tests:

5 suppliers
15 components
3 products
30 purchase orders
20 production orders
50 customer orders
Standard

The primary numbers defined above.

Stress

Approximately 5–10 times standard transactional volume, while preserving the same master-data ratios.

Deliverables
Plain Text
docs/data/scale-and-distribution-specification.md
config/scales/tiny.yaml
config/scales/standard.yaml
config/scales/stress.yaml
9. Phase 3E: Identifier, Serialization and Versioning Standards
Goal

Make generated data human-readable, stable, and safe to load.

Identifier conventions

Use deterministic IDs:

Plain Text
SUP-0001 Supplier
CMP-0001 Component
PRD-0001 Product
BOM-0001-V01 BOM version
WH-PUNE Warehouse
FAC-PUNE Facility
PO-000001 Purchase order
MO-000001 Manufacturing/production order
CO-000001 Customer order
COL-000001-01 Customer-order line
EVT-000001 Event
SCN-0001 Scenario
INT-0001-A Intervention

The Phase 2 golden identifiers may remain as aliases or be normalized consistently. Do not maintain two incompatible identifier systems.

Serialization standards
CSV
UTF-8
Header row required
ISO 8601 timestamps
Decimal point as .
Empty field for nullable value
No formulas
No thousands separators
Explicit booleans, preferably true and false
JSON
UTF-8
Valid JSON Schema where practical
ISO 8601 timestamps
Fixed enum strings
Explicit null
Stable key naming using snake_case
Time

Store:

Plain Text
2026-11-11T02:30:00Z

Display:

Plain Text
2026-11-11 08:00 Asia/Kolkata
Dataset version

Use semantic-like dataset versioning:

Plain Text
chronosdb-dataset-v1.0.0
Major version

Breaking domain or semantic change.

Minor version

Backward-compatible added records or scenarios.

Patch version

Correction that does not change intended benchmark semantics.

If a patch alters expected benchmark outcomes, it is at least a minor change and must be explicitly documented.

Manifest

Every release must contain:

JSON
{
"dataset_name": "chronosdb-synthetic-supply-chain",
"version": "1.0.0",
"generator_version": "1.0.0",
"domain_model_version": "2.0",
"random_seed": 260311,
"generated_at": "ISO-8601 timestamp",
"scale": "standard",
"currency": "INR",
"canonical_timezone": "UTC"
}
Deliverables
Plain Text
docs/data/identifier-and-serialization-standard.md
data/manifest.json
10. Phase 3F: Deterministic Generation Architecture
Goal

Ensure the same inputs always generate the same records.

Generation contract

The generator must be controlled by:

Generator version
Configuration files
Random seed
Domain-model version
Scale selection

Recommended primary seed:

Plain Text
260311

Meaning can be documented as an arbitrary project seed. Do not derive it from sensitive information.

Required generation stages
Plain Text
1. Load configuration
2. Initialize deterministic random generators
3. Generate locations
4. Generate facilities and warehouses
5. Generate suppliers
6. Generate components
7. Generate supplier-component agreements
8. Generate products and BOMs
9. Generate customers
10. Generate historical demand
11. Generate purchase orders
12. Generate production orders
13. Generate customer orders
14. Generate inventory events
15. Derive inventory snapshots
16. Generate historical disruptions
17. Generate evidence documents
18. Inject benchmark scenarios
19. Calculate expected outcomes
20. Validate all invariants
21. Export datasets
22. Generate checksums and statistics
Randomness isolation

Use separate deterministic random streams:

Plain Text
master_data_seed
demand_seed
supply_seed
inventory_seed
disruption_seed
document_seed
benchmark_seed

This prevents a small change in supplier generation from unexpectedly changing every customer order.

Generator requirements
No network access
No system-time-dependent record values except release metadata
No unseeded randomness
Stable ordering before export
Explicit precision and rounding
Fail-fast validation
Actionable error messages
Non-zero exit on failure
Recommended command contract
Shell
make data-generate SCALE=standard SEED=260311
make data-validate
make ground-truth
make data-report
make data-checksums
Reproducibility test

Generate the dataset twice in separate directories.

After excluding permitted volatile metadata:

Plain Text
SHA-256 checksums must match for every data file.
Deliverables
Plain Text
src/data_generator/
config/generation.yaml
scripts/generate_dataset.py
scripts/validate_dataset.py
scripts/build_ground_truth.py
11. Phase 3G: Master-Data Generation
Goal

Generate structurally coherent domain master data.

11.1 Locations

Generate:

Regions
Warehouses
Facilities
Allowed warehouse-to-facility relationships
Transfer lanes

Each transfer lane needs:

Plain Text
source_warehouse
destination_warehouse
lead_time_hours
fixed_cost
variable_cost_per_unit
active_from
active_to
11.2 Suppliers

Generate:

Stable identifiers
Synthetic names
Regions
Active status
Effective dates

Avoid real company names.

Example synthetic names:

NovaCircuit Components
Meridian Micro Systems
Vardhan Industrial Electronics
BlueArc Sensor Works
11.3 Components

Ensure:

Unique ID
Canonical unit
Criticality
Standard unit cost
Safety-stock policy
Optional substitution group
11.4 Supplier-component agreements

Enforce:

Effective approval
Unique active relationship per supplier and component
Positive price
Positive lead time
Capacity
Minimum-order constraint
Currency consistency
11.5 Products and BOMs

Ensure:

Every active product has one active BOM at any time.
Every BOM has at least one line.
Every BOM line references an active component.
Quantity is positive.
No duplicate component line exists within one BOM.
Effective intervals do not overlap.
11.6 Customers and SLAs

Generate synthetic customers with:

Customer class
SLA class
Delivery lead-time rule
Priority
Effective intervals
Deliverables
Plain Text
data/generated/master/
├── suppliers.csv
├── components.csv
├── supplier_component_agreements.csv
├── products.csv
├── bom_versions.csv
├── bom_lines.csv
├── warehouses.csv
├── facilities.csv
├── transfer_lanes.csv
├── customers.csv
└── sla_policies.csv
Master-data invariants
Orphan references: 0
Duplicate primary IDs: 0
Invalid units: 0
Invalid currencies: 0
Overlapping active BOM versions: 0
Products without active BOM: 0
Active components without any valid supply path: allowed only when deliberately labelled as a benchmark condition
12. Phase 3H: Operational and Transactional Data Generation
Goal

Generate connected supply, production, inventory, and customer demand.

12.1 Demand generation

Recommended process:

Generate customer-order demand by product.
Group demand into planned production orders.
Explode production demand through active BOMs.
Determine component requirements.
Generate procurement needed to satisfy projected demand.
Derive inventory movements and balances.

This is better than independently generating every table because it preserves causal consistency.

12.2 Customer orders

Generate:

Order timestamp
Customer
Product
Quantity
Promised delivery
Priority
Unit revenue
Status

Ensure:

Promised delivery is after order time.
Unit revenue is positive.
Product is valid at order time.
Priority follows customer and scenario rules.
12.3 Production orders

Generate from demand:

Plain Text
planned_quantity
facility
planned_start
planned_completion
priority
associated_customer_lines

Capacity should be consumed realistically across the planning horizon.

12.4 Purchase orders

Generate from projected component demand using:

Available inventory
Safety stock
Expected future demand
Supplier lead time
Supplier capacity
Minimum order quantity
12.5 Inventory transactions

Generate events such as:

Plain Text
OPENING_BALANCE
PURCHASE_RECEIPT
PRODUCTION_ISSUE
PRODUCTION_RETURN
TRANSFER_DISPATCH
TRANSFER_RECEIPT
QUARANTINE
RELEASE_FROM_QUARANTINE
ADJUSTMENT

Inventory snapshots should be derived from these transactions, not independently randomized.

12.6 Conservation rule

For every component and warehouse:

EndingBalance=OpeningBalance+Receipts+TransfersIn+PositiveAdjustments−ProductionIssues−TransfersOut−NegativeAdjustmentsEndingBalance = OpeningBalance + Receipts + TransfersIn + PositiveAdjustments - ProductionIssues - TransfersOut - NegativeAdjustmentsEndingBalance=OpeningBalance+Receipts+TransfersIn+PositiveAdjustments−ProductionIssues−TransfersOut−NegativeAdjustments

Any unexplained difference invalidates the dataset.

Deliverables
Plain Text
data/generated/operational/
├── customer_orders.csv
├── customer_order_lines.csv
├── production_orders.csv
├── production_customer_allocations.csv
├── purchase_orders.csv
├── inventory_transactions.csv
├── inventory_snapshots.csv
└── production_material_requirements.csv
13. Phase 3I: Historical and Temporal Data Construction
Goal

Support historical reconstruction and replay rather than only a current-state snapshot.

Historical requirements

Generate at least:

180 days of purchase-order history
180 days of inventory events
180 days of production history
180 days of customer-order history
Past supplier delays
Historical disruptions
Master-data version changes
Temporal patterns

Include:

Supplier agreement becoming active
Supplier agreement expiring
BOM version change
Component safety-stock update
Customer SLA change
Purchase-order status transition
Production-order progress
Inventory correction entered after event time
Bitemporal fixture

At least one controlled scenario should distinguish:

When an event actually occurred
When it became known to the system

Example:

Plain Text
Physical count occurred:
8 Nov, 17:00 IST
 
Correction reported:
9 Nov, 10:00 IST
 
Record ingested:
9 Nov, 10:05 IST

A scenario as of 8 Nov must not use future knowledge.

Snapshot strategy

Use:

Full opening snapshot at the beginning of history
Transaction events throughout the period
Daily derived snapshots
Exact event-state reconstruction around benchmark scenarios
Temporal validation
No state exists before entity activation.
Inactive relationships are not used.
No event consumes future data.
Scenario replay returns the frozen information state.
Effective intervals are half-open.
Late data affects only later information states.
Deliverables
Plain Text
data/generated/history/
├── entity_versions.csv
├── status_events.csv
├── daily_inventory_snapshots.csv
├── supplier_performance_history.csv
├── historical_disruptions.csv
└── late_arriving_corrections.csv
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
15. Phase 3K: Evidence-Document Corpus
Goal

Create an original text corpus for later Db2 vector, semantic, and hybrid retrieval.

Document categories
Supplier notices

Examples:

Full plant shutdown
Partial component interruption
Shipment delay
Recovery update
Capacity limitation
Standard operating procedures
Alternate-supplier approval
Emergency inventory transfer
Purchase-order expedition
Production-priority change
Customer escalation
Historical incident reports

Each should contain:

Incident summary
Affected supplier
Components
Operational impact
Intervention
Outcome
Lessons learned
Policies
Customer SLA definition
Safety-stock protection
Spending approval limits
Supplier qualification requirements
Decision-audit policy
Corpus scale

Recommended:

Document type	Count
Supplier notices	60
Historical incidents	60
Procedures	15
Policies	10
Recovery summaries	30
Total	175

With chunking, this should produce several hundred retrieval units.

Document metadata

Every document must include:

Plain Text
document_id
document_type
title
effective_from
effective_to
status
supplier_id
component_ids
region
incident_type
confidentiality_class
version
created_at
source_type
Retrieval relevance sets

For each retrieval benchmark query, define:

Directly relevant documents
Partially relevant documents
Irrelevant documents
Documents that should be filtered out
Expired documents
Unauthorized documents
Contamination controls

Do not generate documents that state the exact expected recommended intervention for the same benchmark scenario. Otherwise, a RAG system may retrieve the answer rather than reason from operational data.

Evidence may explain policy and historical context, but ground truth must come from structured records and deterministic calculations.

Deliverables
Plain Text
data/generated/documents/
├── supplier_notices/
├── incident_reports/
├── procedures/
├── policies/
├── recovery_summaries/
├── document_metadata.jsonl
└── retrieval_relevance.json
16. Phase 3L: Golden-Scenario Correction and Freeze
Goal

Convert the Phase 2 worked example into a fully consistent machine-readable fixture.

Important correction from Phase 2

Phase 2 refined Chennai inventory to:

Plain Text
On hand: 700 MCU units
Committed local demand: 180
Safety stock: 120
Transferable quantity: 400

This corrected value must replace the earlier 500-unit value everywhere.

Golden scenario identifier
Plain Text
SCN-GOLD-001
Locked scenario input
Plain Text
As-of time:
11 Nov 2026, 08:00 IST
02:30 UTC
 
Disruption:
S-104 full outage
 
Duration:
14 days
 
Recovery lag:
2 days
 
Simulation horizon:
30 days
 
Objective:
MINIMIZE_SLA_BREACHES
 
Budget:
₹200,000
Golden scenario data
Component
Plain Text
CMP-MCU-42
Product
Plain Text
PRD-CONTROLLER-X
BOM
Plain Text
2 × CMP-MCU-42 per finished unit
Pune inventory
Plain Text
400 units
Safety stock: 100
Chennai inventory
Plain Text
700 units
Local committed demand: 180
Safety stock: 120
Maximum transferable: 400
Delayed purchase order
Plain Text
PO-2208
800 units
Original arrival: 13 Nov
Disrupted arrival: 27 Nov
Production orders
Plain Text
MO-0876: 200 products, 400 MCU
MO-0882: 200 products, 400 MCU
MO-0889: 200 products, 400 MCU
Customer orders
Plain Text
CO-0701: ₹800,000
CO-0704: ₹800,000
CO-0711: ₹800,000
Golden scenario calculation correction

The precise production schedule must follow the locked capacity model.

Assume:

Plain Text
Facility capacity:
100 finished units per calendar day
 
Material required:
Fully available at batch start
 
Batch size:
100 units
 
Delivery lead time:
1 calendar day
Baseline before disruption

PO-2208 arrives on 13 Nov.

Expected:

MO-0876 receives existing material.
MO-0882 can use new receipt.
MO-0889 can use remaining receipt.
All orders meet their promised dates under the planned schedule.
Do-nothing after outage
MO-0876 uses existing 400 MCU.
MO-0882 and MO-0889 wait for PO-2208.
PO-2208 becomes available on 27 Nov.
Capacity determines sequential completion.

The exact start and completion convention must specify whether a two-day order starting at 27 Nov completes:

Plain Text
End of 28 Nov

or:

Plain Text
29 Nov

Recommended interval convention:

A 200-unit order at 100 units/day beginning at 27 Nov 00:00 completes at 29 Nov 00:00.

Therefore:

Plain Text
MO-0882:
Start 27 Nov 00:00
Complete 29 Nov 00:00
Deliver 30 Nov 00:00
 
MO-0889:
Start 29 Nov 00:00
Complete 1 Dec 00:00
Deliver 2 Dec 00:00

Expected:

Plain Text
CO-0701: on time
CO-0704: late
CO-0711: late
Breached customer orders: 2
Revenue at risk: ₹1,600,000
Candidate calculations
Candidate A: Transfer 400 MCU

Transfer arrival:

Plain Text
13 Nov

Cost:

₹40,000+400×₹50=₹60,000₹40,000 + 400 \times ₹50 = ₹60,000₹40,000+400×₹50=₹60,000

Expected effect:

Rescues one of the two delayed production orders.
One customer order remains exposed.
Candidate B: Alternate supplier 400 MCU

Arrival:

Plain Text
16 Nov

Premium:

400×(₹1,180−₹1,000)=₹72,000400 \times (₹1,180-₹1,000) = ₹72,000400×(₹1,180−₹1,000)=₹72,000

Expected effect:

Rescues one production order.
One customer order remains exposed.
Exact SLA status depends on capacity and promised dates.
Candidate C: Hybrid
Plain Text
Transfer 400 MCU
+
Alternate procurement of 400 MCU

Cost:

₹60,000+₹72,000=₹132,000₹60,000 + ₹72,000 = ₹132,000₹60,000+₹72,000=₹132,000

Expected, subject to final scheduling calculation:

Plain Text
Breached orders: 0
Revenue at risk: ₹0
Revenue protected: ₹1,600,000
Recommended intervention: Hybrid
Freeze rule

Do not freeze the expected JSON until:

The timeline is calculated hour by hour.
Inventory conservation passes.
Facility-capacity conservation passes.
Two independent reviewers reproduce the values.
Every output has a causal trace.
The recommendation remains within the ₹200,000 budget.

Golden deliverables
Plain Text
data/golden/
├── manifest.json
├── master_data/
├── operational_state/
├── scenario.json
├── interventions.json
├── expected_do_nothing.json
├── expected_interventions.json
├── expected_recommendation.json
├── expected_causal_traces.json
├── manual_workbook.csv
└── review_signoff.md
17. Phase 3M: Benchmark Scenario Suite
Goal

Build a frozen evaluation set broad enough to measure correctness without diluting the core supplier-outage focus.

Recommended 60-scenario suite
Scenario category	Count
Full supplier outage	18
Partial supplier outage	8
Selected-component outage	6
Purchase-order-specific disruption	4
Inventory-transfer constraint	4
Alternate-supplier constraint	4
Budget-constrained recovery	4
No operational impact	3
No feasible intervention	3
Insufficient critical data	3
Tie or Pareto-equivalent outcome	3
Total	60
Difficulty split
Plain Text
Level 1: 15 scenarios
Level 2: 20 scenarios
Level 3: 17 scenarios
Level 4: 8 scenarios
Outcome labels

Each scenario must include:

Plain Text
expected_validity
expected_affected_components
expected_shortages
expected_affected_production_orders
expected_affected_customer_orders
expected_sla_breaches
expected_revenue_at_risk
expected_candidate_feasibility
expected_candidate_metrics
expected_optimal_set
expected_recommendation
expected_data_quality_state
expected_causal_trace_roots
Multiple valid recommendations

Do not force a single expected recommendation when:

Candidates tie
Multiple candidates are Pareto-efficient
Objective weights create equivalent scores

Use:

JSON
{
"expected_optimal_set": [
"INT-SCN-0042-B",
"INT-SCN-0042-D"
],
"tie": true
}
Dataset partitions

Recommended:

Partition	Scenarios
Development	24
Validation	12
Test	18
Golden	3
Adversarial-only	3

The golden scenarios may also be referenced separately from the 60 broad scenarios, but duplication must be explicit.

Deliverables
Plain Text
data/benchmarks/
├── scenarios/
├── expected/
├── partitions.json
├── benchmark_manifest.json
└── scenario_catalogue.csv
18. Phase 3N: Ground-Truth Oracle
Goal

Generate expected outcomes independently from future application services.

The ground-truth oracle is the most important part of Phase 3.

Independence requirement

The Phase 5 production impact engine must not simply import its expected outputs from the oracle.

Recommended separation:

Plain Text
src/ground_truth/
src/application/

The oracle should prioritize clarity and correctness over speed.

Oracle responsibilities
Reconstruct state at the scenario as-of time.
Apply the disruption.
Calculate outstanding receipt changes.
Build inventory timelines.
Allocate components.
Schedule production.
Allocate finished products to customer lines.
Calculate delivery and SLA status.
Calculate revenue at risk.
Apply candidate overlays.
Validate feasibility.
Calculate candidate outcomes.
Rank feasible candidates.
Emit causal traces.
Emit expected outcomes.
Oracle design

Use small, explicit functions:

Plain Text
select_active_records()
calculate_outstanding_quantity()
apply_supplier_outage()
build_inventory_timeline()
allocate_material()
schedule_production()
allocate_customer_fulfilment()
calculate_sla()
calculate_revenue_at_risk()
validate_intervention()
apply_intervention()
rank_candidates()
build_causal_trace()
Explainability requirement

The oracle must emit intermediate calculations, not only final metrics.

Example:

JSON
{
"component_id": "CMP-MCU-42",
"warehouse_id": "WH-PUNE",
"opening_balance": 400,
"receipts": [],
"consumption": [
{
"production_order_id": "MO-0876",
"quantity": 400,
"time": "2026-11-12T00:00:00Z"
}
],
"first_shortage_time": "2026-11-15T00:00:00Z",
"shortage_quantity": 400
}
Numerical determinism
Use decimal arithmetic for money.
Avoid binary floating point for financial values.
Define timestamp boundaries.
Use stable sort keys.
Use explicit rounding.
Hash input state and outputs.
Ground-truth review

For all scenarios:

Automated invariant validation

For golden scenarios:

Full manual validation

For test scenarios:

At least sample-based independent review
Deliverables
Plain Text
src/ground_truth/
tests/ground_truth/
artifacts/ground_truth/
19. Phase 3O: Negative, Boundary and Adversarial Fixtures
Goal

Ensure later systems fail safely rather than producing plausible nonsense.

Required categories
Invalid entity references
Unknown supplier
Unknown component
Unknown warehouse
Unknown production order
Unknown scenario
Invalid quantities
Negative inventory
Zero ordered quantity
Negative disruption duration
Transfer exceeding source stock
Completed quantity exceeding planned quantity
Invalid time
Arrival before order
Scenario before entity activation
Promised delivery before customer order
Outage end before start
Overlapping BOM versions
Missing critical data
No active BOM
No inventory snapshot
Missing promised date
Missing supplier approval
Missing intervention cost
Contradictions
Supplier marked inactive but agreement active
Purchase order marked received with outstanding quantity
Inventory transaction and snapshot disagree
Production completed without required materials
Transfer receipt without dispatch
Optimization traps
Cheapest intervention violates SLA minimum
Best SLA intervention exceeds budget
Two candidates tie
No feasible candidate
Candidate improves one order but harms a higher-priority order
Negative supplier premium due to cheaper alternate supply
Retrieval traps
Expired policy that appears highly relevant
Unauthorized incident report
Historical incident mentioning same supplier but unrelated component
Prompt injection inside a synthetic supplier notice
Document claiming an operational fact contradicted by structured records
Expected error labels
Plain Text
UNKNOWN_ENTITY
INVALID_QUANTITY
INVALID_INTERVAL
MISSING_CRITICAL_DATA
CONTRADICTORY_STATE
INFEASIBLE_INTERVENTION
NO_FEASIBLE_INTERVENTION
INSUFFICIENT_DATA
UNAUTHORIZED_EVIDENCE
EXPIRED_EVIDENCE
Deliverables
Plain Text
data/fixtures/
├── invalid/
├── boundary/
├── adversarial/
└── expected_errors.json
20. Phase 3P: Data Validation and Invariant Enforcement
Goal

Automatically prove dataset integrity.

Validation levels
Level 1: Schema validation

Check:

Required fields
Types
Enum values
Nullability
Decimal precision
Timestamp format
Level 2: Referential validation

Check:

All foreign references exist.
Version references exist.
Scenario entities exist.
Documents reference valid metadata where required.
Level 3: Domain validation

Check:

Positive quantities
Valid statuses
Temporal intervals
Non-overlapping versions
Approved supply relationships
Valid BOMs
Level 4: Conservation validation

Check:

Inventory conservation
Production bounds
Allocation bounds
Customer quantity bounds
Financial bounds
Level 5: Temporal validation

Check:

No future knowledge leakage
Valid effective records
Receipts consumed only after arrival
Events ordered consistently
Level 6: Benchmark validation

Check:

Expected output exists for every frozen scenario.
Every expected recommendation is feasible.
Every expected output has provenance.
Every test scenario belongs to exactly one partition.
Critical invariants
Inventory
Ending=Opening+In−OutEnding = Opening + In - OutEnding=Opening+In−Out
Purchase order
0≤ReceivedQuantity≤OrderedQuantity0 \le ReceivedQuantity \le OrderedQuantity0≤ReceivedQuantity≤OrderedQuantity
Production order
0≤CompletedQuantity≤PlannedQuantity0 \le CompletedQuantity \le PlannedQuantity0≤CompletedQuantity≤PlannedQuantity
Customer line
0≤OnTimeQuantity+LateQuantity≤OrderedQuantity0 \le OnTimeQuantity + LateQuantity \le OrderedQuantity0≤OnTimeQuantity+LateQuantity≤OrderedQuantity
Revenue at risk
0≤RevenueAtRisk≤OpenOrderRevenue0 \le RevenueAtRisk \le OpenOrderRevenue0≤RevenueAtRisk≤OpenOrderRevenue
Transfer
TransferQuantity≤TransferableQuantityTransferQuantity \le TransferableQuantityTransferQuantity≤TransferableQuantity
Budget

For feasible interventions:

InterventionCost≤MaximumRecoveryBudgetInterventionCost \le MaximumRecoveryBudgetInterventionCost≤MaximumRecoveryBudget
Validation severity
Plain Text
ERROR:
Release-blocking
 
WARNING:
Allowed only with documented reason
 
INFO:
Statistical or descriptive observation
Required result
Plain Text
Validation errors: 0
Undocumented warnings: 0
Deliverables
Plain Text
schemas/
validation/
artifacts/data-validation-report.json
artifacts/data-validation-report.md
21. Phase 3Q: Statistical and Realism Assessment
Goal

Ensure data is neither trivially uniform nor accidentally impossible.

Required descriptive statistics
Supply
Suppliers per component
Lead-time distribution
Price distribution
Capacity distribution
Approval distribution
Product structure
Components per BOM
BOM critical-component count
Product-family demand
Inventory
Days of coverage
Safety-stock ratio
Stockout frequency
Warehouse concentration
Operations
Production utilization
Purchase-order arrival performance
Customer-order size
Customer priority
SLA lead time
Late order rate
Disruptions
Duration
Scope
Affected records
Severity
Feasible intervention count
Impact level
Realism thresholds

Avoid:

Every component having exactly two suppliers
Every purchase order using the same quantity
Every customer order having identical revenue
Perfect historical delivery
Uniform disruption impact
All scenarios having a feasible solution
One intervention type always winning
Benchmark balance checks

Recommended constraints:

No single intervention wins more than 45% of solvable scenarios.
At least 10% of scenarios have no operational impact.
At least 5% have no feasible intervention.
At least 5% contain critical insufficient data.
At least 20% require more than simple direct dependency traversal.
At least 20% have competing objectives.
Test scenarios cover every intervention type.

These are design targets, not facts about real supply chains.

Distribution comparison

Compare generated distributions against configuration targets.

Example:

DistributionDeviation=∣ObservedShare−TargetShare∣DistributionDeviation = |ObservedShare - TargetShare|DistributionDeviation=∣ObservedShare−TargetShare∣

Recommended tolerance:

Plain Text
±5 percentage points for major categorical distributions
Deliverables
Plain Text
artifacts/dataset-statistics.json
artifacts/dataset-statistics.md
artifacts/distribution-checks.json
22. Phase 3R: Privacy, Licensing and Contamination Controls
Goal

Ensure the dataset is safe to publish and evaluate.

Privacy rules
No real people
No real customer records
No personal email addresses
No phone numbers
No addresses tied to individuals
No employer-confidential information
No private procurement data
No private pricing
No copied incident reports
Naming rules

All organization, supplier, and customer names must be:

Artificially generated
Clearly fictional
Reviewed for accidental real-company collision where practical
Document licensing

Preferred approach:

Generate all documents specifically for the project.
License project-authored dataset and documents consistently with repository policy.
Include attribution only for external standards or public references actually used.
Do not copy IBM documentation into the corpus.
Contamination controls

Prevent:

Expected-answer text inside evidence documents
Scenario IDs inside unrelated documents
Recommendation labels leaking into raw inputs
Test expected outputs appearing in development prompts
Ground-truth JSON being loaded into application retrieval
Dataset declaration

Create a dataset card stating:

Synthetic origin
Intended use
Prohibited interpretation
Known limitations
Generation method
Version
Benchmark partitions
No claim of representing real enterprise performance
Deliverable
Plain Text
docs/data/DATASET_CARD.md
docs/data/privacy-and-licensing-review.md
23. Phase 3S: Dataset Packaging and Reproducibility
Goal

Deliver data in a stable structure ready for Db2 ingestion.

Recommended structure
Plain Text
data/
├── README.md
├── manifest.json
├── checksums.sha256
├── generated/
│ ├── master/
│ ├── operational/
│ ├── history/
│ ├── scenarios/
│ └── documents/
├── golden/
├── benchmarks/
├── fixtures/
└── reports/
Required commands
Shell
make data-clean
make data-generate SCALE=standard SEED=260311
make data-validate
make ground-truth
make data-report
make data-checksums
make data-all

make data-all should:

Remove previous generated output safely.
Generate the dataset.
Generate the evidence corpus.
Build benchmark scenarios.
Calculate expected outcomes.
Validate all records.
Produce statistics.
Generate checksums.
Exit non-zero if any required check fails.
Build isolation

Do not overwrite:

Manually curated configuration
Frozen benchmark definitions
Golden manual calculations
Review signoff

Generated artifacts and curated source inputs must live separately.

Provenance manifest

For every generated file, record:

Plain Text
path
record_count
sha256
generator_stage
configuration
random_seed
schema_version
Reproducibility drill

On a clean checkout:

Install dependencies.
Run make data-all.
Compare checksums.
Run validation.
Compare golden outputs.
Record runtime and hardware.
Targets
Metric	Target
Clean generation success	100%
Validation errors	0
Checksum mismatch	0
Manual edits to generated files	0
Undocumented build step	0
Golden output mismatch	0
24. Phase 3T: Dataset Benchmark and Quality Score
Goal

Quantify whether the dataset is suitable for implementation and evaluation.

24.1 Referential integrity
RI=valid foreign referencesall foreign referencesRI = \frac{\text{valid foreign references}} {\text{all foreign references}}RI=all foreign referencesvalid foreign references​

Target:

Plain Text
100%
24.2 Domain validity
DV=records satisfying domain rulesrecords subject to domain rulesDV = \frac{\text{records satisfying domain rules}} {\text{records subject to domain rules}}DV=records subject to domain rulesrecords satisfying domain rules​

Target:

Plain Text
100%
24.3 Temporal validity
TV=valid temporal relationshipsall checked temporal relationshipsTV = \frac{\text{valid temporal relationships}} {\text{all checked temporal relationships}}TV=all checked temporal relationshipsvalid temporal relationships​

Target:

Plain Text
100%
24.4 Ground-truth coverage
GTC=frozen scenarios with complete expected outcomesall frozen scenariosGTC = \frac{\text{frozen scenarios with complete expected outcomes}} {\text{all frozen scenarios}}GTC=all frozen scenariosfrozen scenarios with complete expected outcomes​

Target:

Plain Text
100%
24.5 Provenance coverage
PC=expected key outputs with complete provenanceall expected key outputsPC = \frac{\text{expected key outputs with complete provenance}} {\text{all expected key outputs}}PC=all expected key outputsexpected key outputs with complete provenance​

Target:

Plain Text
100%
24.6 Reproducibility
Reproducibility=matching deterministic filesall deterministic output filesReproducibility = \frac{\text{matching deterministic files}} {\text{all deterministic output files}}Reproducibility=all deterministic output filesmatching deterministic files​

Target:

Plain Text
100%
24.7 Partition integrity

Target:

Scenario in multiple exclusive partitions: 0
Test answer leakage into input corpus: 0
Test case used for parameter tuning: 0 documented instances
24.8 Retrieval benchmark readiness

Target:

Queries with relevance labels: at least 50
Relevant documents per query: at least one, except explicit no-match tests
Expired-document filter tests: at least 10
Unauthorized-document filter tests: at least 10
Prompt-injection document tests: at least five
Phase 3 scorecard
Category	Weight
Domain-model conformity	15
Referential and temporal integrity	15
Generator determinism	12
Operational realism	10
Golden scenario correctness	15
Benchmark breadth	10
Ground-truth quality	10
Evidence corpus quality	5
Privacy and licensing	4
Packaging and reproducibility	4
Total	100
Passing threshold
Plain Text
95–100: Pass
90–94: Conditional pass
Below 90: Fail
Automatic failures

Phase 3 fails regardless of score if:

Golden outputs disagree between reviewers.
Inventory conservation fails.
A benchmark recommendation violates a hard constraint.
Expected outcomes are missing.
Generated data contains real private information.
The generator is nondeterministic.
Test-answer leakage is found.
Missing values are silently converted to zero.
Referential-integrity errors remain.
Phase 4 would require manual repair.
Expected outputs are copied into evidence documents.
Dataset version and checksum manifest are absent.
25. Phase 3U: Independent Review and Release Freeze
Goal

Review the dataset from multiple practitioner perspectives.

Required reviews
Domain review

Verify:

Relationships are realistic enough for the MVP.
Supply constraints are meaningful.
Interventions obey physical limits.
Revenue language remains accurate.
Data-engineering review

Verify:

Referential integrity
Stable identifiers
Reproducibility
Schema consistency
Missing-value handling
Export safety
Temporal review

Verify:

Effective intervals
Event and ingestion times
Snapshot reconstruction
No future leakage
Benchmark review

Verify:

Scenario diversity
Expected outcomes
No obvious shortcut
No leakage
Correct partitions
Fair baselines
Security and privacy review

Verify:

Synthetic identities
No secrets
No personal information
No private documents
No unlicensed corpus content
Freeze process

Once accepted:

Set dataset version to 1.0.0.
Generate final artifacts.
Produce checksums.
Store validation reports.
Mark test outcomes read-only.
Record the source commit.
Create release notes.
Freeze the benchmark partition file.
Prevent accidental regeneration with another seed.
Hand the manifest to Phase 4.
Release identity
Plain Text
Dataset:
chronosdb-synthetic-supply-chain
 
Version:
1.0.0
 
Seed:
260311
 
Release label:
phase-3-dataset-v1.0.0
Deliverables
Plain Text
docs/data/review-signoff.md
docs/data/release-notes-v1.0.0.md
artifacts/phase-3-release-manifest.json
26. Phase 3 Execution Order

Follow this order. Do not generate large datasets before validating tiny examples and the golden scenario.

Work Block 1: Handoff and contracts
Plain Text
3A. Validate Phase 2 artifacts
3A. Resolve remaining domain decisions
3B. Freeze dataset objectives
3B. Freeze benchmark partitions
3B. Define leakage controls
Work Block 2: Enterprise and scale
Plain Text
3C. Define synthetic organization
3C. Define network and product families
3D. Define entity counts
3D. Define distributions
3D. Define tiny, standard and stress scales
Work Block 3: Standards and generator
Plain Text
3E. Lock identifiers
3E. Lock file formats
3E. Lock versioning
3F. Design generation stages
3F. Isolate random streams
3F. Implement deterministic configuration
Work Block 4: Tiny dataset first
Plain Text
3G. Generate tiny master data
3H. Generate tiny operational data
3I. Generate short history
3P. Validate all invariants

Do not proceed until tiny-scale validation has zero errors.

Work Block 5: Golden scenario
Plain Text
3L. Encode the corrected golden scenario
3N. Implement the transparent oracle
3L. Calculate baseline
3L. Calculate do-nothing
3L. Calculate each intervention
3L. Independently review results
3L. Freeze expected outputs
Work Block 6: Standard dataset
Plain Text
3G. Generate standard master data
3H. Generate operations
3I. Build temporal history
3J. Generate disruptions and interventions
3K. Generate the evidence corpus
Work Block 7: Benchmarks
Plain Text
3M. Construct 60 scenarios
3M. Assign difficulty levels
3M. Freeze partitions
3N. Calculate ground truth
3N. Generate causal traces
3O. Add invalid and adversarial fixtures
Work Block 8: Validation and realism
Plain Text
3P. Run schema validation
3P. Run referential validation
3P. Run domain invariants
3P. Run temporal validation
3P. Run conservation checks
3Q. Calculate descriptive statistics
3Q. Compare observed and target distributions
3Q. Correct generator configuration

Do not manually edit generated records to make statistics appear better. Correct the generator or configuration.

Work Block 9: Safety and packaging
Plain Text
3R. Run privacy review
3R. Run licensing review
3R. Check benchmark leakage
3S. Package files
3S. Generate manifests
3S. Generate checksums
3S. Run clean reproducibility drill
Work Block 10: Freeze and handoff
Plain Text
3T. Calculate Phase 3 score
3U. Run independent review
3U. Resolve release-blocking defects
3U. Freeze dataset v1.0.0
3V. Prepare Phase 4 load contract
27. Required Phase 3 Repository Structure
Plain Text
config/
├── enterprise.yaml
├── generation.yaml
├── scales/
│ ├── tiny.yaml
│ ├── standard.yaml
│ └── stress.yaml
└── scenarios/
 
src/
├── data_generator/
│ ├── config.py
│ ├── random_streams.py
│ ├── master_data.py
│ ├── demand.py
│ ├── procurement.py
│ ├── production.py
│ ├── inventory.py
│ ├── history.py
│ ├── disruptions.py
│ ├── documents.py
│ └── export.py
└── ground_truth/
├── state.py
├── disruption.py
├── inventory.py
├── scheduling.py
├── customer_impact.py
├── interventions.py
├── ranking.py
└── provenance.py
 
schemas/
├── csv/
├── json/
└── validation/
 
data/
├── README.md
├── manifest.json
├── checksums.sha256
├── generated/
├── golden/
├── benchmarks/
├── fixtures/
└── reports/
 
tests/
├── data_generator/
├── ground_truth/
├── invariants/
└── reproducibility/
 
docs/data/
├── phase-2-handoff-review.md
├── dataset-and-benchmark-contract.md
├── synthetic-enterprise-blueprint.md
├── scale-and-distribution-specification.md
├── identifier-and-serialization-standard.md
├── DATASET_CARD.md
├── privacy-and-licensing-review.md
├── release-notes-v1.0.0.md
├── review-signoff.md
├── phase-3-traceability-matrix.csv
└── phase-3-completion-report.md
 
artifacts/
├── data-validation-report.json
├── dataset-statistics.json
├── distribution-checks.json
├── ground-truth-review.json
└── phase-3-release-manifest.json
28. Phase 3 Traceability Matrix

Create:

Plain Text
docs/data/phase-3-traceability-matrix.csv

Recommended columns:

Plain Text
phase2_rule_id
domain_entity
generated_file
generator_module
configuration_key
validation_rule
benchmark_scenario_ids
expected_output_field
ground_truth_function
phase4_target_table
status
notes

Example:

Plain Text
INV-TRANSFER-001,
Warehouse inventory,
inventory_snapshots.csv,
inventory.py,
safety_stock_ratio,
VAL-INV-008,
SCN-0012|SCN-0034,
expected_candidate_feasibility,
validate_transfer(),
INVENTORY_SNAPSHOT,
APPROVED,
Source safety stock enforced
29. Phase 3 Final Gate Checklist
Handoff and semantics
 All Phase 2 model inputs are present.
 Partial production is explicitly defined.
 Partial delivery is explicitly defined.
 Production-capacity behavior is defined.
 Material-consumption timing is defined.
 No data-generation rule contradicts Phase 2.
Enterprise and scale
 Synthetic organization is documented.
 Network structure is documented.
 Product and component families are documented.
 Tiny scale is defined.
 Standard scale is defined.
 Stress scale is defined.
 Distribution targets are documented.
Generation
 Generator uses explicit seeds.
 Random streams are isolated.
 Stable identifiers are used.
 Stable export ordering is used.
 No network access is required.
 Same inputs produce identical outputs.
 Generated files are never manually corrected.
Master data
 Supplier records are valid.
 Supplier agreements are valid.
 Components have canonical units.
 Products have active BOMs.
 BOM intervals do not overlap.
 Warehouses and facilities are valid.
 Transfer lanes are valid.
 Customer SLA rules are valid.
Operational data
 Customer demand drives production.
 Production drives material requirements.
 Material requirements drive procurement.
 Inventory transactions reconcile.
 Purchase-order quantities reconcile.
 Production quantities reconcile.
 Customer allocations reconcile.
Temporal data
 Historical period is complete.
 Effective intervals are valid.
 Event time and ingestion time are distinct.
 Late-arriving data tests exist.
 Scenario replay prevents future leakage.
 Snapshots reconcile with transactions.
Evidence documents
 Corpus is original.
 Metadata is complete.
 Effective dates are present.
 Expired-document fixtures exist.
 Unauthorized-document fixtures exist.
 Prompt-injection fixtures exist.
 Expected answers do not leak into documents.
 Retrieval relevance labels exist.
Golden scenario
 Corrected Chennai inventory is used.
 Baseline is calculated.
 Do-nothing result is calculated.
 Transfer candidate is calculated.
 Alternate-supplier candidate is calculated.
 Hybrid candidate is calculated.
 Exact scheduling boundaries are frozen.
 Inventory conservation passes.
 Capacity conservation passes.
 Two reviewers agree.
 Golden JSON outputs are frozen.
Benchmark suite
 Sixty scenarios exist.
 Difficulty levels are assigned.
 Development partition exists.
 Validation partition exists.
 Test partition exists.
 Adversarial partition exists.
 No scenario appears in incompatible partitions.
 Multiple valid answers are represented correctly.
 No test-answer leakage exists.
Ground truth
 Oracle is separate from application code.
 Intermediate calculations are emitted.
 Decimal arithmetic is used.
 Stable tie-breaking is used.
 Every expected result has provenance.
 Every expected recommendation is feasible.
 All frozen scenarios have expected outcomes.
Validation
 Schema errors are zero.
 Referential errors are zero.
 Domain errors are zero.
 Conservation errors are zero.
 Temporal errors are zero.
 Undocumented warnings are zero.
 Dataset statistics are generated.
 Distribution deviations are within tolerance.
Privacy and release
 Dataset is fully synthetic.
 No personal data exists.
 No confidential enterprise data exists.
 No copied incident reports exist.
 Dataset card is complete.
 Manifest is present.
 Checksums are present.
 Clean reproducibility drill passes.
 Dataset version is frozen.
 Phase 3 score is at least 95.
 No automatic-failure condition remains.
30. Phase 3V: Phase 4 Handoff
Next phase
Phase 4: IBM Db2 Data Architecture and Physical Schema
Phase 4 goal

Translate the valid Phase 3 dataset and Phase 2 domain model into a production-quality Db2 architecture covering:

Operational relational tables
Temporal history
Scenario persistence
Simulation outcomes
Evidence documents
Vector storage
Audit records
Constraints
Roles
Indexes
Migrations
Seed loading
Query plans
Data lifecycle
Mandatory Phase 4 inputs
Models
Entity model
Relationship model
Temporal model
State transitions
Provenance model
Data assets
Dataset v1.0.0
Manifest
Checksums
Golden scenario
Benchmark suite
Negative fixtures
Evidence corpus
Validation assets
Schemas
Domain invariants
Referential rules
Temporal validation rules
Conservation rules
Load-contract fields

For every generated file, Phase 4 must receive:

Plain Text
source_file
record_type
primary_key
foreign_keys
data_types
nullability
unique_constraints
check_constraints
temporal_columns
currency_columns
quantity_columns
expected_target_table
load_order
expected_row_count
checksum
Required Phase 4 load order

Conceptually:

Plain Text
1. Reference types
2. Locations
3. Suppliers and components
4. Supplier-component agreements
5. Products and BOMs
6. Customers and SLA policies
7. Transfer lanes
8. Inventory history
9. Purchase orders
10. Production orders
11. Customer orders
12. Disruptions
13. Scenarios
14. Evidence documents
15. Benchmark metadata

The actual table and migration design will be finalized in Phase 4.

Final Phase 3 Outcome

When Phase 3 passes, ChronosDB will have more than demonstration data. It will have a controlled evaluation asset:

Every record follows the domain model.
Every operational quantity reconciles.
Every historical scenario respects time.
Every recommendation has a known correct outcome.
Every benchmark case has ground truth.
Every document is original and labelled.
Every build is reproducible.
Every file is versioned and checksummed.
Every future metric can be computed against a frozen test suite.

Phase 4 can then focus entirely on designing the IBM Db2 data architecture and physical schema, without repairing data or redefining business rules.