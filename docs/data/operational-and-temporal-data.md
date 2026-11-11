# Phase 3H–3I: Operational and Temporal Data

Operational records are generated causally in this order:

`customer orders → production orders → BOM requirements → purchase orders → inventory transactions → snapshots`

Customer and production identifiers are stable and all foreign keys point to
Phase 3G master records. Inventory snapshots are derived from opening balances
and ordered transaction events; they are never independently randomized.

History uses the configured 180-day window and daily snapshots. Effective
intervals are half-open and timestamps are UTC. The bitemporal fixture records
event time, known-at time, and ingestion time separately so a scenario as of
the physical event cannot use a later correction.
