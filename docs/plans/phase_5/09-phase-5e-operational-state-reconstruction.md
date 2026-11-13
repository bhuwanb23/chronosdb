9. Phase 5E: Operational-State Reconstruction
Goal

Create the exact state known and valid at the scenario's as-of timestamp.

State-input classes
Effective master data
Active suppliers
Active agreements
Active products
Active BOM versions
Active SLA policies
Operational state
Inventory
Outstanding purchase orders
Production status
Customer-order status
Facility capacity
Information state

Records known by the system at the scenario time.

State-selection rule

A record is eligible when:

effective_from≤as_of<effective_toeffective\_from \le as\_of < effective\_toeffective_from≤as_of<effective_to

and:

ingested_time≤as_ofingested\_time \le as\_ofingested_time≤as_of

when information-time control applies.

Inventory reconstruction

Recommended approach:

Load latest valid checkpoint at or before as_of_time.
Apply ledger events after the checkpoint and through as_of_time.
Reconcile the calculated state.
Compare with an available benchmark snapshot when present.
Fail or warn on unexplained mismatch.
Purchase-order reconstruction

At the scenario time, determine:

Ordered quantity
Received quantity
Outstanding quantity
Current expected arrival
Current status
Active supplier
Destination warehouse
Production reconstruction

Determine:

Planned quantity
Completed quantity
Remaining quantity
Material previously issued
Current state
Locked batches
Future material demand
Customer reconstruction

Determine:

Open quantity
Fulfilled quantity
Remaining quantity
Promised time
Associated production demand
Priority
State hash

Canonicalize all impact-relevant records:

Plain Text
sort records by entity type and stable identifier
normalize timestamps to UTC
normalize decimal serialization
remove non-semantic metadata
serialize deterministically
calculate SHA-256
State-reconstruction result
JSON
{
"state_version": "STATE-GOLD-001",
"as_of_time": "...",
"state_hash": "...",
"record_counts": {},
"completeness": "COMPLETE",
"warnings": []
}
Deliverables
Plain Text
src/backend/chronosdb/impact/state/
docs/impact-engine/state-reconstruction.md
Acceptance criteria
Golden-state hash matches Phase 4.
Ten historical reconstruction fixtures match exactly.
Late-arriving data is excluded when appropriate.
Expired BOM and agreements are excluded.
No future event leaks into the reconstructed state.
