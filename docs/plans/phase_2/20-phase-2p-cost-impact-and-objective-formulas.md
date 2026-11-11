20. Phase 2P: Cost, Impact and Objective Formulas
Goal

Freeze mathematical definitions before code and data generation.

20.1 Core impact metrics
Affected components

A component is affected when the disruption changes at least one expected receipt or causes a projected shortage relative to the no-disruption baseline.

Maintain both:

Plain Text
Supply-affected components
Shortage-affected components
Affected production order

A production order is affected when its projected start or completion changes because of the disruption.

Affected customer order

A customer order is affected when at least one line has a changed projected delivery date.

SLA breach

A customer order is projected to breach when at least one required order line is late under the defined fulfilment rule.

Total delay

Recommended customer-impact measure:

TotalDelayHours=∑lLateQuantityl×DelayHourslTotalDelayHours = \sum_l LateQuantity_l \times DelayHours_lTotalDelayHours=l∑​LateQuantityl​×DelayHoursl​

This is quantity-weighted delay.

Also report:

Plain Text
Maximum customer delay
Average breached-line delay
Breached-order count
20.2 Cost metrics
Transfer cost
TransferCost=FixedTransferCost+Quantity×VariableCostPerUnitTransferCost = FixedTransferCost + Quantity \times VariableCostPerUnitTransferCost=FixedTransferCost+Quantity×VariableCostPerUnit
Expedite cost
ExpediteCost=FixedExpediteFee+OutstandingQuantity×ExpediteCostPerUnitExpediteCost = FixedExpediteFee + OutstandingQuantity \times ExpediteCostPerUnitExpediteCost=FixedExpediteFee+OutstandingQuantity×ExpediteCostPerUnit
Alternate supplier premium
AlternatePremium=Quantity×max⁡(0,AlternateUnitPrice−BaselineUnitPrice)AlternatePremium = Quantity \times \max(0, AlternateUnitPrice - BaselineUnitPrice)AlternatePremium=Quantity×max(0,AlternateUnitPrice−BaselineUnitPrice)

If the alternate supplier is cheaper, record savings separately rather than allowing negative intervention cost to distort comparisons.

Rescheduling cost

MVP may use a fixed, documented cost per affected production-order change.

20.3 Revenue protected
RevenueProtectedi=max⁡(0,RevenueAtRiskDoNothing−RevenueAtRiski)RevenueProtected_i = \max( 0, RevenueAtRisk_{DoNothing} - RevenueAtRisk_i )RevenueProtectedi​=max(0,RevenueAtRiskDoNothing​−RevenueAtRiski​)
20.4 Net protected value

Optional explanatory metric:

NetProtectedValuei=RevenueProtectedi−InterventionCostiNetProtectedValue_i = RevenueProtected_i - InterventionCost_iNetProtectedValuei​=RevenueProtectedi​−InterventionCosti​

Do not treat this as profit because revenue at risk is not guaranteed loss.

20.5 Objective modes
Minimize SLA breaches

Lexicographic ranking:

Fewest breached customer orders
Lowest revenue at risk
Lowest intervention cost
Lowest total delay
Stable intervention ID
Minimize revenue at risk
Lowest revenue at risk
Fewest SLA breaches
Lowest cost
Lowest delay
Minimize recovery cost
Lowest intervention cost
Subject to service-level constraint
Lowest revenue at risk
Lowest delay
Balanced recovery

Use normalized metrics:

Scorei=wsSi+wrRi+wdDi+wcCiScore_i = w_s S_i + w_r R_i + w_d D_i + w_c C_iScorei​=ws​Si​+wr​Ri​+wd​Di​+wc​Ci​

Where each normalized value is in [0,1][0,1][0,1], and lower is better.

Suggested default weights:

Plain Text
SLA breach score: 0.40
Revenue-at-risk score: 0.30
Delay score: 0.20
Recovery-cost score: 0.10

Weights must sum to 1.

Normalization

For metric xxx:

Normalized(xi)=xi−min⁡(x)max⁡(x)−min⁡(x)Normalized(x_i) = \frac{x_i - \min(x)} {\max(x) - \min(x)}Normalized(xi​)=max(x)−min(x)xi​−min(x)​

If all candidates have equal values:

Normalized(xi)=0Normalized(x_i) = 0Normalized(xi​)=0
20.6 Hard constraints before ranking

A candidate violating a hard constraint is excluded from recommendation ranking.

Hard constraints include:

Approval
Capacity
Inventory
Budget
Safety stock
Time horizon
Valid state transition
Deliverables
Plain Text
docs/domain/formula-catalogue.md
docs/domain/objective-and-ranking-model.md
Formula gate

Every formula must identify:

Formula ID
Inputs
Units
Output
Preconditions
Rounding
Edge cases
Example
Owning requirement
Future implementation phase
