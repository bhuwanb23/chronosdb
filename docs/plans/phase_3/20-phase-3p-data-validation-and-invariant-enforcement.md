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
