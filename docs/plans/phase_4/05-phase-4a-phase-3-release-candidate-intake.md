5. Phase 4A: Phase 3 Release-Candidate Intake
Goal

Confirm that the Phase 3 generator and data contract are ready to produce the release dataset.

Required inputs

Verify:

Plain Text
config/enterprise.yaml
config/generation.yaml
config/scales/tiny.yaml
config/scales/standard.yaml
config/scales/stress.yaml
 
src/data_generator/
src/ground_truth/
 
schemas/
tests/data_generator/
tests/ground_truth/
tests/invariants/
 
docs/data/DATASET_CARD.md
docs/data/dataset-and-benchmark-contract.md
docs/data/phase-3-completion-report.md
Required locked decisions
Decision	Locked value
Organization	Asterion Control Systems
Industry	Industrial electronics
Currency	INR
Stored timezone	UTC
Display timezone	Asia/Kolkata
Primary scenario	Critical supplier outage
Planning horizon	30 calendar days
Historical period	180 days
Quantity arithmetic	Decimal
Financial arithmetic	Fixed decimal
Primary seed	260311
Standard dataset version	1.0.0
Ground-truth authority	Deterministic oracle
Missing-value behavior	Never implicit zero
Intake checks
Generator executes on tiny scale.
Tiny data passes all critical invariants.
Ground-truth oracle executes separately from product code.
Golden-scenario correction is present.
Dataset partitions are defined.
Evidence documents cannot leak expected answers.
All Phase 3 blocking defects are closed.
Deliverable
Plain Text
docs/dataset-release/phase-3-intake-report.md
Exit gate

Phase 4A fails if:

The generator is nondeterministic.
The golden scenario is unresolved.
Partial production semantics remain ambiguous.
Inventory reconciliation is not implemented.
Expected outcomes are manually entered without derivation or review.
