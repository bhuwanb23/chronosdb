17. Phase 5M: SLA and Revenue-Impact Engine
Goal

Calculate business exposure from projected customer fulfilment.

SLA status

For each delivery segment:

Plain Text
ON_TIME
BREACHED
INSUFFICIENT_DATA

Optional warning state:

Plain Text
AT_RISK

AT_RISK must not be counted as an actual projected breach unless the formal policy says so.

Delay calculation
DelayHoursl=max⁡(0,ProjectedDeliveryl−PromisedDeliveryl)DelayHours_l = \max( 0, ProjectedDelivery_l - PromisedDelivery_l )DelayHoursl​=max(0,ProjectedDeliveryl​−PromisedDeliveryl​)
Revenue at risk
RevenueAtRiskl=LateQuantityl×UnitRevenuelRevenueAtRisk_l = LateQuantity_l \times UnitRevenue_lRevenueAtRiskl​=LateQuantityl​×UnitRevenuel​
Total revenue at risk
TotalRevenueAtRisk=∑lRevenueAtRisklTotalRevenueAtRisk = \sum_l RevenueAtRisk_lTotalRevenueAtRisk=l∑​RevenueAtRiskl​
Quantity-weighted delay
WeightedDelayHours=∑lLateQuantityl×DelayHourslWeightedDelayHours = \sum_l LateQuantity_l \times DelayHours_lWeightedDelayHours=l∑​LateQuantityl​×DelayHoursl​
Breach metrics

Report:

Breached order-line count
Breached customer-order count
Late product quantity
Revenue at risk
Maximum delay
Average delay among late segments
Quantity-weighted delay
Revenue bounds

For every line:

0≤RevenueAtRiskl≤OpenQuantityl×UnitRevenuel0 \le RevenueAtRisk_l \le OpenQuantity_l \times UnitRevenue_l0≤RevenueAtRiskl​≤OpenQuantityl​×UnitRevenuel​
Golden expected headline

The locked Phase 4 result should produce:

Plain Text
Breached customer orders: 2
Revenue at risk: ₹1,600,000

All detailed timing and delay values must match the frozen expected timeline exactly.

Deliverables
Plain Text
src/backend/chronosdb/impact/financial/
src/backend/chronosdb/impact/fulfilment/sla.py
docs/impact-engine/sla-and-financial-impact.md
