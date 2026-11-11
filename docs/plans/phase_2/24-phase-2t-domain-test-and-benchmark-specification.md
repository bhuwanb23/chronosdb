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
