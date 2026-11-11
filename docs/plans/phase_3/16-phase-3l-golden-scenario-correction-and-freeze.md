16. Phase 3L: Golden-Scenario Correction and Freeze
Goal

Convert the Phase 2 worked example into a fully consistent machine-readable fixture.

Important correction from Phase 2

Phase 2 refined Chennai inventory to:

Plain Text
On hand: 700 MCU units
Committed local demand: 180
Safety stock: 120
Transferable quantity: 400

This corrected value must replace the earlier 500-unit value everywhere.

Golden scenario identifier
Plain Text
SCN-GOLD-001
Locked scenario input
Plain Text
As-of time:
11 Nov 2026, 08:00 IST
02:30 UTC
 
Disruption:
S-104 full outage
 
Duration:
14 days
 
Recovery lag:
2 days
 
Simulation horizon:
30 days
 
Objective:
MINIMIZE_SLA_BREACHES
 
Budget:
₹200,000
Golden scenario data
Component
Plain Text
CMP-MCU-42
Product
Plain Text
PRD-CONTROLLER-X
BOM
Plain Text
2 × CMP-MCU-42 per finished unit
Pune inventory
Plain Text
400 units
Safety stock: 100
Chennai inventory
Plain Text
700 units
Local committed demand: 180
Safety stock: 120
Maximum transferable: 400
Delayed purchase order
Plain Text
PO-2208
800 units
Original arrival: 13 Nov
Disrupted arrival: 27 Nov
Production orders
Plain Text
MO-0876: 200 products, 400 MCU
MO-0882: 200 products, 400 MCU
MO-0889: 200 products, 400 MCU
Customer orders
Plain Text
CO-0701: ₹800,000
CO-0704: ₹800,000
CO-0711: ₹800,000
Golden scenario calculation correction

The precise production schedule must follow the locked capacity model.

Assume:

Plain Text
Facility capacity:
100 finished units per calendar day
 
Material required:
Fully available at batch start
 
Batch size:
100 units
 
Delivery lead time:
1 calendar day
Baseline before disruption

PO-2208 arrives on 13 Nov.

Expected:

MO-0876 receives existing material.
MO-0882 can use new receipt.
MO-0889 can use remaining receipt.
All orders meet their promised dates under the planned schedule.
Do-nothing after outage
MO-0876 uses existing 400 MCU.
MO-0882 and MO-0889 wait for PO-2208.
PO-2208 becomes available on 27 Nov.
Capacity determines sequential completion.

The exact start and completion convention must specify whether a two-day order starting at 27 Nov completes:

Plain Text
End of 28 Nov

or:

Plain Text
29 Nov

Recommended interval convention:

A 200-unit order at 100 units/day beginning at 27 Nov 00:00 completes at 29 Nov 00:00.

Therefore:

Plain Text
MO-0882:
Start 27 Nov 00:00
Complete 29 Nov 00:00
Deliver 30 Nov 00:00
 
MO-0889:
Start 29 Nov 00:00
Complete 1 Dec 00:00
Deliver 2 Dec 00:00

Expected:

Plain Text
CO-0701: on time
CO-0704: late
CO-0711: late
Breached customer orders: 2
Revenue at risk: ₹1,600,000
Candidate calculations
Candidate A: Transfer 400 MCU

Transfer arrival:

Plain Text
13 Nov

Cost:

₹40,000+400×₹50=₹60,000₹40,000 + 400 \times ₹50 = ₹60,000₹40,000+400×₹50=₹60,000

Expected effect:

Rescues one of the two delayed production orders.
One customer order remains exposed.
Candidate B: Alternate supplier 400 MCU

Arrival:

Plain Text
16 Nov

Premium:

400×(₹1,180−₹1,000)=₹72,000400 \times (₹1,180-₹1,000) = ₹72,000400×(₹1,180−₹1,000)=₹72,000

Expected effect:

Rescues one production order.
One customer order remains exposed.
Exact SLA status depends on capacity and promised dates.
Candidate C: Hybrid
Plain Text
Transfer 400 MCU
+
Alternate procurement of 400 MCU

Cost:

₹60,000+₹72,000=₹132,000₹60,000 + ₹72,000 = ₹132,000₹60,000+₹72,000=₹132,000

Expected, subject to final scheduling calculation:

Plain Text
Breached orders: 0
Revenue at risk: ₹0
Revenue protected: ₹1,600,000
Recommended intervention: Hybrid
Freeze rule

Do not freeze the expected JSON until:

The timeline is calculated hour by hour.
Inventory conservation passes.
Facility-capacity conservation passes.
Two independent reviewers reproduce the values.
Every output has a causal trace.
The recommendation remains within the ₹200,000 budget.

Golden deliverables
Plain Text
data/golden/
├── manifest.json
├── master_data/
├── operational_state/
├── scenario.json
├── interventions.json
├── expected_do_nothing.json
├── expected_interventions.json
├── expected_recommendation.json
├── expected_causal_traces.json
├── manual_workbook.csv
└── review_signoff.md
