18. Phase 2N: Intervention Model
Goal

Define how recovery actions alter the disrupted scenario.

18.1 Do nothing
State change

None.

Purpose

Provides the required disrupted baseline for all comparisons.

18.2 Warehouse inventory transfer
Inputs
Plain Text
source_warehouse
destination_warehouse
component
quantity
transfer_start
transfer_lead_time
transfer_cost
Hard constraints
Source inventory exists.
Transfer does not violate protected safety stock.
Quantity is positive.
Destination is eligible.
Arrival occurs within simulation horizon.
Material is not already allocated elsewhere.
State changes
Plain Text
Source projected balance decreases at dispatch.
Destination projected balance increases at arrival.
Transfer cost is added.
18.3 Expedite purchase order
Inputs
Plain Text
purchase_order
new_arrival_time
expedite_cost
Hard constraints
Purchase order is outstanding.
Purchase order is expedite-eligible.
New arrival precedes disrupted arrival.
Supplier outage does not make expedition physically impossible.
Cost is within budget.
State changes
Plain Text
Receipt timestamp changes.
Expedite cost is added.

Important: Expediting cannot magically override a total supplier outage unless the order had already left the supplier or the model explicitly supports another logistics path.

18.4 Alternate supplier
Inputs
Plain Text
alternate_supplier
component
quantity
order_time
lead_time
unit_price
Hard constraints
Supplier-component relationship is approved.
Agreement is effective.
Quantity satisfies minimum order.
Quantity does not exceed capacity.
Arrival falls within horizon.
Cost is within budget.
Cost
AlternateSupplyCost=Quantity×AlternateUnitPriceAlternateSupplyCost = Quantity \times AlternateUnitPriceAlternateSupplyCost=Quantity×AlternateUnitPrice

Incremental intervention cost should compare against normal expected procurement cost:

SupplierPremium=Quantity×(AlternateUnitPrice−BaselineUnitPrice)SupplierPremium = Quantity \times (AlternateUnitPrice - BaselineUnitPrice)SupplierPremium=Quantity×(AlternateUnitPrice−BaselineUnitPrice)

If the alternative replaces an existing purchase, avoid counting full purchase cost as purely incremental.

18.5 Production rescheduling
Inputs
Plain Text
affected_production_order
new_priority
new_sequence
reschedule_cost
Hard constraints
Order is not completed.
Locked in-progress work is not preempted.
Facility capacity remains valid.
Rescheduling does not create hidden infeasibility.
Any new customer impact is included.
State changes

Production priority and capacity allocation change.

The model must calculate both:

Orders helped
Orders harmed

18.6 Hybrid intervention

Recommended first hybrid:

Plain Text
Warehouse transfer
+
Alternate supplier

The combination must be simulated as one intervention, not by adding separate outcome metrics.

18.7 Feasibility status
Plain Text
FEASIBLE
INFEASIBLE
INSUFFICIENT_DATA
UNSUPPORTED
18.8 Rejection codes

Examples:

Plain Text
SOURCE_SAFETY_STOCK_VIOLATION
INSUFFICIENT_TRANSFERABLE_QUANTITY
SUPPLIER_NOT_APPROVED
SUPPLIER_CAPACITY_EXCEEDED
MINIMUM_ORDER_NOT_MET
RECOVERY_BUDGET_EXCEEDED
PO_NOT_EXPEDITE_ELIGIBLE
OUTAGE_PREVENTS_EXPEDITION
ARRIVAL_OUTSIDE_HORIZON
PRODUCTION_ORDER_LOCKED
MISSING_REQUIRED_DATA
Deliverable
Plain Text
docs/domain/intervention-model.md
docs/domain/feasibility-rule-catalogue.md
Exit gate
Every intervention has explicit parameters.
Every intervention has hard constraints.
Every intervention has deterministic state changes.
Infeasibility has a machine-readable reason.
An intervention cannot create material from nothing.
