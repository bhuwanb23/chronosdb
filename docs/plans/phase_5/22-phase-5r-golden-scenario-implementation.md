22. Phase 5R: Golden-Scenario Implementation
Goal

Make the frozen golden scenario pass exactly before evaluating the broad suite.

Golden execution steps
Step 1: Reconstruct state

As of:

Plain Text
11 Nov 2026, 08:00 IST

Verify:

Plain Text
WH-PUNE CMP-MCU-42 available: 400
WH-CHENNAI CMP-MCU-42:
700 on hand
180 protected local demand
120 safety stock
400 transferable, although transfer is not applied in Phase 5
Step 2: Apply disruption
Plain Text
SUP-0104 unavailable for 14 days
Recovery lag: 2 days
PO-2208 moves from 13 Nov to 27 Nov
Step 3: Allocate existing Pune material
Plain Text
MO-0876 requires 400 MCU
Existing Pune inventory: 400
MO-0876 receives allocation
Remaining projected available MCU: 0
Step 4: Detect shortage
Plain Text
MO-0882 and MO-0889 cannot obtain required MCU
until delayed PO-2208 arrives
Step 5: Reschedule production

Use:

100-unit batches
200 MCU per batch
100 finished units per day
Stable priority queue
Step 6: Calculate customer fulfilment
Plain Text
CO-0701 remains on time
CO-0704 becomes late
CO-0711 becomes late
Step 7: Calculate exposure
Plain Text
Breached customer orders: 2
Late revenue:
₹800,000 + ₹800,000
= ₹1,600,000
Step 8: Produce causal traces

Each late order must trace through:

Plain Text
outage
→ PO-2208
→ CMP-MCU-42 shortage
→ manufacturing order
→ customer order
→ SLA breach
→ revenue at risk
Golden acceptance requirement

All fields must match the Phase 4 frozen expected result:

Exact timestamps
Exact quantities
Exact delay hours
Exact breach counts
Exact revenue
Exact causal parents
Exact rule IDs
Exact attribution classes
Golden-first rule

Do not special-case golden identifiers in implementation.

Prohibited:

Python
if scenario_id == "SCN-GOLD-001":
return expected_result

The golden scenario must pass through the same engine used for every benchmark case.

Deliverables
Plain Text
tests/impact/golden/
artifacts/phase-5/golden-impact-result.json
artifacts/phase-5/golden-comparison-report.md

