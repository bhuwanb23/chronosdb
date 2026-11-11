12. Phase 4H: Customer-Demand and SLA Production
Goal

Create customer demand that is traceable to production and financially coherent.

Customer-order header fields
Plain Text
customer_order_id
customer_id
order_time
promised_delivery_time
priority
sla_class
status
currency
Customer-order line fields
Plain Text
customer_order_line_id
customer_order_id
product_id
ordered_quantity
fulfilled_quantity
unit_revenue
assigned_production_order_id
Revenue invariant
LineRevenue=OrderedQuantity×UnitRevenueLineRevenue = OrderedQuantity \times UnitRevenueLineRevenue=OrderedQuantity×UnitRevenue
Allocation rule

Customer lines are allocated using:

Customer priority
Promised delivery time
Order time
Stable order ID
Required examples

The dataset must contain:

Fully on-time orders
Partially fulfilled orders
Late orders
High-priority orders
Orders protected by an intervention
Orders harmed by careless rescheduling
Orders unaffected by the primary disruption
Golden customer orders
Order	Qty.	Unit revenue	Total revenue	Promised
CO-0701	200	₹4,000	₹800,000	15 Nov
CO-0704	200	₹4,000	₹800,000	18 Nov
CO-0711	200	₹4,000	₹800,000	21 Nov
Ground-truth fields

For frozen scenarios, derive:

Plain Text
projected_on_time_quantity
projected_late_quantity
projected_delivery_time
delay_hours
sla_status
revenue_at_risk
Revenue at risk
RevenueAtRisk=LateQuantity×UnitRevenueRevenueAtRisk = LateQuantity \times UnitRevenueRevenueAtRisk=LateQuantity×UnitRevenue

Do not label this amount as confirmed loss.

Deliverables
Plain Text
data/releases/v1.0.0/demand/
├── customer_orders.csv
├── customer_order_lines.csv
├── customer_order_status_history.csv
├── production_customer_allocations.csv
└── customer_sla_assignments.csv
