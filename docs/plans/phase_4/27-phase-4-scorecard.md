27. Phase 4 Scorecard
Category	Weight
Master-data coherence	8
Procurement-data quality	8
Inventory reconciliation	12
Production and capacity consistency	10
Customer and financial consistency	10
Temporal-history correctness	10
Golden-scenario correctness	15
Benchmark completeness	10
Evidence-corpus quality	5
Privacy and leakage protection	5
Reproducibility and packaging	7
Total	100
Passing threshold
Plain Text
95–100: Pass
90–94: Conditional pass
Below 90: Fail
Automatic failures

Phase 4 fails regardless of score if:

Any golden headline value is unverified.
Inventory conservation fails.
Facility capacity is exceeded without explanation.
A feasible expected recommendation violates a hard constraint.
Test answers appear in the evidence corpus.
Generated data contains real private information.
A deterministic file changes between identical builds.
Test partitions overlap improperly.
Referential-integrity errors remain.
Missing data is replaced with zero.
Dataset loading requires undocumented manual repair.
Golden scenario depends on hardcoded application behavior.
Expected results cannot be traced to source records.
Release checksums are missing.
