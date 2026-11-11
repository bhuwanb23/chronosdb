22. Phase 4R: Realism and Distribution Validation
Goal

Verify that the demonstration data behaves like an interconnected operational environment rather than random noise.

Structural measures

Calculate:

Suppliers per component
Components per BOM
Products per component
Purchase orders per supplier
Customer lines per product
Production orders per facility
Inventory coverage by component
Operational measures

Calculate:

Facility capacity utilization
Order volume by week
Inventory turnover proxy
Average days of inventory
Purchase-order lateness
Supplier concentration
Stockout frequency
SLA breach rate
Alternate-supplier coverage
Scenario measures

Calculate:

Affected component count
Affected production-order count
Affected customer-order count
Revenue-at-risk distribution
Feasible candidate count
Winning intervention distribution
No-action recommendation frequency
No-feasible-plan rate
Required dataset behaviors

The standard dataset should contain:

High-impact and low-impact suppliers
Single-source and multi-source components
High- and low-priority customers
Adequate and inadequate inventory coverage
Feasible and infeasible interventions
Short and long disruptions
Scenarios where no action is best
Scenarios where the cheapest option is not best
Scenarios where the best operational option exceeds budget
Scenarios with multiple valid optima
Anti-pattern detection

Fail or warn if:

Every supplier has the same lead time.
Every BOM contains the same number of components.
Every order quantity is a round identical value.
Every intervention is feasible.
Hybrid intervention always wins.
No-action never wins.
All customer orders have the same value.
Historical operations are perfect.
Every scenario affects the same number of orders.
Target benchmark diversity
Measure	Target
Intervention types represented	5/5
No-impact scenarios	≥5%
No-feasible scenarios	≥5%
Insufficient-data scenarios	≥5%
Multiple-optimum scenarios	≥5%
Temporal reconstruction scenarios	≥15%
Partial-fulfilment scenarios	≥10%
Multi-product impact scenarios	≥20%
Deliverables
Plain Text
artifacts/phase-4/realism/
├── dataset-profile.json
├── distribution-analysis.json
├── scenario-diversity.json
└── realism-review.md
