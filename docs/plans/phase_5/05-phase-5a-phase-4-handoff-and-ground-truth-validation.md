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
