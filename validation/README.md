# Phase 3 Validation Contract

Release validation is implemented by
`src/data_generator/release_validation.py` and exposed through
`scripts/validate_release.py`. Findings are classified as `ERROR`, `WARNING`,
or `INFO`; release output requires zero errors and zero undocumented warnings.

The validation layers are:

1. Serialized schema, field, timestamp, and nullability checks.
2. Referential joins across master, operations, history, scenarios, and evidence.
3. Domain rules for quantities, statuses, intervals, BOMs, and approved supply.
4. Inventory, production, allocation, financial, transfer, and budget conservation.
5. Effective-time, event ordering, and bitemporal correction checks.
6. Benchmark coverage, provenance, feasibility, and partition checks.
