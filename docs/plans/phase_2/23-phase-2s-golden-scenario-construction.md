23. Phase 2S: Golden Scenario Construction
Goal

Create one fully worked example that validates the entire model.

This scenario becomes the foundation for:

Phase 3 dataset generation
Phase 4 schema validation
Phase 5 impact-engine testing
Phase 6 simulation testing
Phase 7 optimization testing
The demo
Benchmark ground truth
23.1 Golden scenario setting
Organization

A synthetic electronics manufacturer.

Facilities
Plain Text
FAC-PUNE

Capacity:

Plain Text
100 finished units per day
Warehouses
Plain Text
WH-PUNE
WH-CHENNAI
Critical component
Plain Text
C-MCU-42

Unit:

Plain Text
EA
Finished product
Plain Text
P-CONTROLLER-X
BOM

Each controller requires:

Plain Text
2 × C-MCU-42

No scrap factor for the golden case.

23.2 Suppliers
Primary supplier
Plain Text
Supplier: S-104
Component: C-MCU-42
Normal lead time: 7 days
Unit price: ₹1,000
Approval: APPROVED
Alternate supplier
Plain Text
Supplier: S-208
Component: C-MCU-42
Lead time: 5 days
Unit price: ₹1,180
Daily capacity: 100 units
Minimum order: 100 units
Approval: APPROVED
23.3 Operational state

Scenario as-of time:

Plain Text
11 Nov 2026, 08:00 IST
Pune inventory
Plain Text
On hand: 400 MCU units
Reserved: 0
Safety stock: 100
Chennai inventory
Plain Text
On hand: 500 MCU units
Committed local demand: 180
Safety stock: 120

Transferable quantity:

500−180−120=200500 - 180 - 120 = 200500−180−120=200

Therefore:

Plain Text
Maximum transferable quantity = 200 MCU units

Transfer lead time:

Plain Text
2 days

Transfer cost:

Plain Text
₹40,000 fixed + ₹50 per unit

For 200 units:

₹40,000+(200×₹50)=₹50,000₹40,000 + (200 \times ₹50) = ₹50,000₹40,000+(200×₹50)=₹50,000
23.4 Purchase order
Plain Text
PO-2208
Supplier: S-104
Component: C-MCU-42
Outstanding quantity: 800 units
Original expected arrival: 13 Nov 2026
Destination: WH-PUNE
23.5 Disruption
Plain Text
Supplier S-104 outage
Start: 11 Nov 2026, 08:00 IST
Duration: 14 days
End: 25 Nov 2026, 08:00 IST
Recovery lag: 2 days

New arrival:

Plain Text
27 Nov 2026
23.6 Production orders
PROD-876
Plain Text
Product: P-CONTROLLER-X
Quantity: 200 units
MCU requirement: 400 units
Planned start: 12 Nov
Planned completion: 14 Nov
Customer line: CO-701-L1
PROD-882
Plain Text
Product: P-CONTROLLER-X
Quantity: 200 units
MCU requirement: 400 units
Planned start: 15 Nov
Planned completion: 17 Nov
Customer line: CO-704-L1
PROD-889
Plain Text
Product: P-CONTROLLER-X
Quantity: 200 units
MCU requirement: 400 units
Planned start: 18 Nov
Planned completion: 20 Nov
Customer line: CO-711-L1

Total MCU requirement:

400+400+400=1,200400 + 400 + 400 = 1,200400+400+400=1,200
23.7 Customer orders
CO-701
Plain Text
Quantity: 200 products
Promised delivery: 15 Nov
Unit revenue: ₹4,000
Order-line revenue: ₹800,000
Priority: HIGH
CO-704
Plain Text
Quantity: 200 products
Promised delivery: 18 Nov
Unit revenue: ₹4,000
Order-line revenue: ₹800,000
Priority: MEDIUM
CO-711
Plain Text
Quantity: 200 products
Promised delivery: 21 Nov
Unit revenue: ₹4,000
Order-line revenue: ₹800,000
Priority: MEDIUM

Total revenue:

₹2,400,000₹2,400,000₹2,400,000
23.8 Do-nothing calculation

Pune starts with:

Plain Text
400 MCU units

PROD-876 consumes:

Plain Text
400 MCU units

Remaining:

Plain Text
0

PO-2208 is delayed until 27 Nov.

Therefore:

PROD-876 remains on schedule.
PROD-882 cannot start until 27 Nov.
PROD-889 must follow capacity scheduling after PROD-882.

With one-day delivery lead time and 100-unit/day production capacity:

PROD-876
Plain Text
Start: 12 Nov
Complete: 14 Nov
Deliver: 15 Nov
CO-701: on time
PROD-882
Plain Text
Start: 27 Nov
Duration: 2 days
Complete: 29 Nov
Deliver: 30 Nov
CO-704 due: 18 Nov
Delay: 12 days
PROD-889
Plain Text
Start: 29 Nov
Duration: 2 days
Complete: 1 Dec
Deliver: 2 Dec
CO-711 due: 21 Nov
Delay: 11 days

Do-nothing result:

Plain Text
Breached orders: 2
Revenue at risk: ₹1,600,000
Quantity-weighted delay:
(200 × 12) + (200 × 11) = 4,600 unit-days
23.9 Candidate A: Transfer 200 MCU units

Arrival at Pune:

Plain Text
13 Nov

This supports:

Plain Text
100 finished products

But a production order requires 400 MCU units for 200 units if partial production is not enabled.

Phase 2 decision

We must explicitly choose whether partial production is allowed.

Recommended MVP decision:

Plain Text
Partial production is allowed in capacity-sized batches.

With 100-product batch:

Transfer supports half of PROD-882.
Production can complete 100 products.
The remaining quantity waits for later supply.
Partial customer delivery can reduce late quantity if allowed.

However, partial delivery adds significant complexity.

Recommended golden-scenario simplification

Increase transferable quantity to:

Plain Text
400 MCU units

To achieve this consistently, revise Chennai inventory:

Plain Text
On hand: 700
Committed demand: 180
Safety stock: 120
Transferable: 400

Use this corrected value for the locked golden scenario.

Transfer cost:

₹40,000+(400×₹50)=₹60,000₹40,000 + (400 \times ₹50) = ₹60,000₹40,000+(400×₹50)=₹60,000

This fully rescues PROD-882.

23.10 Candidate B: Alternate supplier

Order:

Plain Text
400 MCU units

Lead time:

Plain Text
5 days

Arrival:

Plain Text
16 Nov

Supplier premium:

400×(₹1,180−₹1,000)=₹72,000400 \times (₹1,180 - ₹1,000) = ₹72,000400×(₹1,180−₹1,000)=₹72,000

This can support one production order.

23.11 Candidate C: Hybrid intervention
Plain Text
Transfer 400 MCU units from Chennai
+
Order 400 MCU units from S-208

Arrivals:

Plain Text
Transfer: 13 Nov
Alternate supplier: 16 Nov

This provides enough material for PROD-882 and PROD-889 before disrupted PO arrival.

Cost:

₹60,000+₹72,000=₹132,000₹60,000 + ₹72,000 = ₹132,000₹60,000+₹72,000=₹132,000

Expected result:

Plain Text
CO-701: on time
CO-704: projected on time or near original plan
CO-711: projected on time or near original plan
Breached orders: 0
Revenue at risk: ₹0
Revenue protected: ₹1,600,000
Intervention cost: ₹132,000

The precise production sequence must be recalculated using the locked material arrival and facility-capacity rules.

23.12 Golden-scenario constraints
Plain Text
Maximum recovery budget: ₹200,000
Objective: Minimize SLA breaches
Approved suppliers only: Yes
Minimum source safety stock: Enforced
Simulation horizon: 30 days
Expected recommendation

Under the proposed values:

Plain Text
Hybrid intervention

Why:

Both affected customer orders can be protected.
The intervention remains under the ₹200,000 budget.
Approved supply is used.
Source safety stock remains protected.
It outperforms single interventions on SLA breaches.
Golden-scenario deliverables
Plain Text
docs/domain/golden-scenario/
├── scenario-definition.md
├── input-records.csv
├── manual-calculation.md
├── do-nothing-result.json
├── intervention-results.json
├── expected-recommendation.json
├── causal-traces.md
└── assumptions.md
Golden-scenario validation rule

At least two independent manual calculations should agree exactly on:

Shortage dates
Affected production orders
Completion dates
Customer delivery dates
SLA breaches
Revenue at risk
Intervention costs
Chosen recommendation
