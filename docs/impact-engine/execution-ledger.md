# Execution Ledger

The execution ledger stores the impact run, request fingerprint, frozen input
state reference, projected supply, inventory timelines, allocations,
shortages, production and customer impacts, metrics, causal traces,
provenance, warnings, errors, and final result hash.

Operational source records are read-only. Calculated projections are stored
separately. Completed results are immutable, repeated fingerprints are
idempotent, and failed runs retain diagnostics for safe retry. The
calculation layer depends on the `ExecutionLedger` contract rather than on a
Db2 client.
