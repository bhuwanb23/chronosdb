8. Phase 3D: Dataset Scale and Distribution Design
Goal

Choose a scale large enough to demonstrate enterprise-like relationships while remaining reproducible and inspectable.

Recommended MVP scale
Entity	Target
Suppliers	24
Supplier-component agreements	120–180
Components	80
Products	16
BOM versions	24–32
BOM lines	160–240
Warehouses	3
Facilities	2
Inventory snapshot rows	12,000–18,000
Purchase orders	600
Production orders	400
Customers	80
Customer orders	1,000
Customer-order lines	1,300–1,800
Disruption events	100
Historical incident reports	60
Operating procedures and policies	25–40
Frozen benchmark scenarios	60
Adversarial fixtures	25–40
Historical period

Recommended generation window:

Plain Text
180 days of history
+
30-day future planning horizon
Inventory snapshot frequency

Recommended default:

Plain Text
Daily snapshots at 00:00 UTC

For the golden scenario and selected benchmarks:

Plain Text
Hourly event-level changes

This balances scale and temporal precision.

Distribution targets
Supplier concentration

Model a realistic dependency mix:

15% of components: single approved supplier
45%: two approved suppliers
30%: three approved suppliers
10%: four or more approved suppliers
Criticality
Critical: 20%
High: 30%
Medium: 35%
Low: 15%
Lead time

Suggested synthetic ranges:

Supplier region	Lead time
Same region	2–5 days
Other Indian region	4–8 days
Southeast/East Asia	8–20 days
Europe	12–25 days

Use configurable distributions rather than hardcoded record-by-record choices.

Product demand

Use a right-skewed distribution:

A small number of high-demand products
Several medium-demand products
Rare low-demand products

A log-normal or gamma distribution is more suitable than a uniform distribution.

Order priority
High: 15%
Medium: 50%
Normal: 35%
Disruption severity
Minor delay: 35%
Partial outage: 30%
Full supplier outage: 25%
Multi-factor or edge case: 10%
Scale tiers

Support at least:

Plain Text
tiny
standard
stress
Tiny

For local tests:

5 suppliers
15 components
3 products
30 purchase orders
20 production orders
50 customer orders
Standard

The primary numbers defined above.

Stress

Approximately 5–10 times standard transactional volume, while preserving the same master-data ratios.

Deliverables
Plain Text
docs/data/scale-and-distribution-specification.md
config/scales/tiny.yaml
config/scales/standard.yaml
config/scales/stress.yaml
