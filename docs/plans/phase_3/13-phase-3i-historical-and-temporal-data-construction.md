13. Phase 3I: Historical and Temporal Data Construction
Goal

Support historical reconstruction and replay rather than only a current-state snapshot.

Historical requirements

Generate at least:

180 days of purchase-order history
180 days of inventory events
180 days of production history
180 days of customer-order history
Past supplier delays
Historical disruptions
Master-data version changes
Temporal patterns

Include:

Supplier agreement becoming active
Supplier agreement expiring
BOM version change
Component safety-stock update
Customer SLA change
Purchase-order status transition
Production-order progress
Inventory correction entered after event time
Bitemporal fixture

At least one controlled scenario should distinguish:

When an event actually occurred
When it became known to the system

Example:

Plain Text
Physical count occurred:
8 Nov, 17:00 IST
 
Correction reported:
9 Nov, 10:00 IST
 
Record ingested:
9 Nov, 10:05 IST

A scenario as of 8 Nov must not use future knowledge.

Snapshot strategy

Use:

Full opening snapshot at the beginning of history
Transaction events throughout the period
Daily derived snapshots
Exact event-state reconstruction around benchmark scenarios
Temporal validation
No state exists before entity activation.
Inactive relationships are not used.
No event consumes future data.
Scenario replay returns the frozen information state.
Effective intervals are half-open.
Late data affects only later information states.
Deliverables
Plain Text
data/generated/history/
├── entity_versions.csv
├── status_events.csv
├── daily_inventory_snapshots.csv
├── supplier_performance_history.csv
├── historical_disruptions.csv
└── late_arriving_corrections.csv
