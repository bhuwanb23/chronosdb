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
