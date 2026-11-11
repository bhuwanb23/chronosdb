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
