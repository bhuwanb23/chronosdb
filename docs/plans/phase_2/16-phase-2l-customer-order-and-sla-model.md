16. Phase 2L: Customer-Order and SLA Model
Goal

Translate production completion into customer impact.

16.1 Fulfilment model

For MVP:

A customer-order line is linked to a production order.
Completed product may fulfil one or more order lines.
Order lines are allocated by defined customer priority.
Shipping transit may use a fixed delivery lead time.

Recommended default:

Plain Text
Delivery lead time = 1 calendar day
16.2 Projected delivery
ProjectedDeliveryl=ProjectedProductAvailabilityl+DeliveryLeadTimelProjectedDelivery_l = ProjectedProductAvailability_l + DeliveryLeadTime_lProjectedDeliveryl​=ProjectedProductAvailabilityl​+DeliveryLeadTimel​
16.3 SLA classification

Recommended classifications:

Plain Text
ON_TIME
AT_RISK
BREACHED
INSUFFICIENT_DATA
During simulation
ON_TIME: projected delivery is on or before promised date.
BREACHED: projected delivery exceeds promised date.
AT_RISK: optional forward-looking warning when margin is below a configured threshold.
INSUFFICIENT_DATA: required date or fulfilment mapping is missing.

For benchmark simplicity, the core binary metric should use:

Plain Text
ON_TIME
BREACHED
16.4 Delay
CustomerDelayHoursl=max⁡(0,ProjectedDeliveryl−PromisedDeliveryl)CustomerDelayHours_l = \max( 0, ProjectedDelivery_l - PromisedDelivery_l )CustomerDelayHoursl​=max(0,ProjectedDeliveryl​−PromisedDeliveryl​)
16.5 Partial fulfilment

For an order line:

LateQuantityl=max⁡(0,OrderedQuantityl−OnTimeFulfilledQuantityl)LateQuantity_l = \max( 0, OrderedQuantity_l - OnTimeFulfilledQuantity_l )LateQuantityl​=max(0,OrderedQuantityl​−OnTimeFulfilledQuantityl​)
16.6 Revenue at risk
RevenueAtRiskl=LateQuantityl×UnitRevenuelRevenueAtRisk_l = LateQuantity_l \times UnitRevenue_lRevenueAtRiskl​=LateQuantityl​×UnitRevenuel​

Total:

TotalRevenueAtRisk=∑lRevenueAtRisklTotalRevenueAtRisk = \sum_l RevenueAtRisk_lTotalRevenueAtRisk=l∑​RevenueAtRiskl​
16.7 SLA breach count

Two separate measures are useful:

Breached order lines
Countlines=∣{l∣LateQuantityl>0}∣Count_{lines} = |\{l \mid LateQuantity_l > 0\}|Countlines​=∣{l∣LateQuantityl​>0}∣
Breached customer orders
Countorders=∣{o∣∃l∈o,LateQuantityl>0}∣Count_{orders} = |\{o \mid \exists l \in o, LateQuantity_l > 0\}|Countorders​=∣{o∣∃l∈o,LateQuantityl​>0}∣

The interface must label which one is shown.

Recommended headline metric:

Plain Text
Projected customer orders breached
Deliverables
Plain Text
docs/domain/customer-fulfilment-model.md
docs/domain/sla-and-revenue-model.md
Exit gate
Partial fulfilment is supported.
Promised date has a clear time zone and granularity.
Revenue at risk applies to late quantity.
Order-line and order-level breach counts are distinct.
Missing due dates produce insufficient data.
