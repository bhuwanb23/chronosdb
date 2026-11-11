13. Phase 4I: Temporal-History Production
Goal

Make historical reconstruction and decision replay possible.

Required time columns

When relevant, records must distinguish:

Plain Text
event_time
reported_time
ingested_time
effective_from
effective_to
recorded_at
Historical fixtures

The release must include:

Supplier agreement activation
Supplier agreement expiry
BOM revision
Safety-stock policy change
Customer SLA change
Purchase-order delay
Partial goods receipt
Inventory correction
Disruption reported after event start
Scenario frozen before a late correction
Bitemporal demonstration case

Example:

Plain Text
Physical count occurred:
8 Nov 2026, 17:00 IST
 
Correction reported:
9 Nov 2026, 10:00 IST
 
Ingested:
9 Nov 2026, 10:05 IST

Required behavior:

A scenario frozen before 10:05 on 9 November does not use the correction.
A later scenario may use it.
An already completed scenario does not change.
Effective interval convention

Use half-open intervals:

[effective_from,effective_to)[effective\_from, effective\_to)[effective_from,effective_to)
Snapshot-reconstruction benchmark

For at least ten historical timestamps:

Reconstruct inventory state from ledger.
Compare to stored snapshot.
Require exact agreement.
Deliverables
Plain Text
data/releases/v1.0.0/history/
├── entity_versions.csv
├── business_events.csv
├── late_arriving_records.csv
├── historical_inventory_checkpoints.csv
└── replay_expectations.json
