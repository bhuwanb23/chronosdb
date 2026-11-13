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
