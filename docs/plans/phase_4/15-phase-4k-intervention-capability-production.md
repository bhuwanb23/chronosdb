15. Phase 4K: Intervention-Capability Production
Goal

Produce the operational records necessary to test recovery actions.

Inventory-transfer data

Required:

Transfer lane
Eligible component
Available quantity
Dispatch time
Lead time
Fixed cost
Variable cost
Safety-stock protection
Expedition data

Required:

Purchase-order eligibility
Earliest achievable arrival
Fixed fee
Variable fee
Outage compatibility

An order cannot be expedited through a complete production outage unless it had already left the supplier or an alternative physical path exists.

Alternate-supplier data

Required:

Approval
Effective interval
Lead time
Available capacity
Minimum order
Unit price
Currency
Component compatibility
Production-rescheduling data

Required:

Order status
Lock status
Priority
Facility capacity
Reschedule penalty
Downstream customer impact
Golden intervention records
Transfer
Plain Text
WH-CHENNAI → WH-PUNE
CMP-MCU-42
Quantity: 400
Lead time: 2 days
Fixed cost: ₹40,000
Variable cost: ₹50/unit
Total: ₹60,000
Alternate supplier
Plain Text
Supplier: SUP-0208
Component: CMP-MCU-42
Quantity: 400
Lead time: 5 days
Unit price: ₹1,180
Baseline unit price: ₹1,000
Incremental premium: ₹72,000
Hybrid
₹60,000+₹72,000=₹132,000₹60,000 + ₹72,000 = ₹132,000₹60,000+₹72,000=₹132,000
Infeasible candidate

Add at least one visually meaningful rejection, for example:

Plain Text
Transfer 500 MCU units from WH-CHENNAI

Expected:

Plain Text
INFEASIBLE
Reason: SOURCE_SAFETY_STOCK_VIOLATION
Maximum transferable quantity: 400
Deliverables
Plain Text
data/releases/v1.0.0/interventions/
├── transfer_capabilities.csv
├── expedite_capabilities.csv
├── alternate_supply_capabilities.csv
├── rescheduling_constraints.csv
└── intervention_cost_parameters.csv
