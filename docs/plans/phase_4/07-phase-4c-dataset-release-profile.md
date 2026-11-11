7. Phase 4C: Dataset Release Profile
Goal

Freeze the exact volume and structure of the released demonstration dataset.

Recommended standard release
Dataset object	Release target
Suppliers	24
Components	80
Supplier-component agreements	150
Products	16
BOM versions	28
BOM lines	190–230
Warehouses	3
Facilities	2
Transfer lanes	6 directional lanes
Customers	80
SLA policies	3–5
Purchase orders	600
Production orders	400
Customer orders	1,000
Customer-order lines	1,400–1,700
Inventory transactions	20,000–35,000
Daily inventory snapshots	12,000–18,000
Historical disruption events	100
Evidence documents	Approximately 175
Frozen benchmark scenarios	60
Negative/adversarial fixtures	At least 30
Release variants
tiny

Purpose:

Unit testing
Fast integration tests
Schema checks
Local developer setup
demo

Purpose:

Stable judge-facing scenario
Presentation
Screenshots
Demo video
Fast setup

This should contain the golden scenario and a controlled subset of supporting records.

standard

Purpose:

Full development
Benchmarking
Retrieval evaluation
Realism assessment
stress

Purpose:

Query and application performance testing
Not required for the primary demo
Critical distinction

Do not use the standard dataset for every demo operation if it makes the demonstration slower or less predictable.

Use:

Plain Text
demo dataset = curated and frozen
standard dataset = broader and statistically varied
stress dataset = scaled performance workload
Deliverable
Plain Text
config/releases/
├── tiny-v1.0.0.yaml
├── demo-v1.0.0.yaml
├── standard-v1.0.0.yaml
└── stress-v1.0.0.yaml
