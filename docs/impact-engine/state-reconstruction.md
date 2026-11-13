# Operational-State Reconstruction

The release loader reads the canonical Phase 4 CSV records, applies effective
interval and information-time predicates, and limits historical ledger/status
events to the requested as-of timestamp. Records are sorted by canonical JSON
before the state SHA-256 is calculated.

Future purchase-order commitments remain in state because they are open
operational facts; historical receipts and status events are limited to the
as-of boundary. Missing required record classes are rejected rather than
silently treated as empty state.
