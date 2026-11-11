25. Phase 2U: Domain Review and Falsification
Goal

Actively attempt to break the model before generating data or code.

25.1 Review perspectives
Supply-chain review

Check:

Is the inventory logic plausible?
Are supplier constraints represented?
Can a recommendation violate physical reality?
Are delayed receipts calculated consistently?
Manufacturing review

Check:

Does production require all mandatory components?
Is facility capacity enforced?
Is completed production protected?
Does rescheduling harm other orders?
Financial review

Check:

Is revenue at risk overstated?
Is partial lateness handled?
Are incremental and total costs separated?
Are currencies consistent?
Temporal review

Check:

Are time intervals unambiguous?
Can records overlap?
Can future data leak into historical scenarios?
Are timezone conversions stable?
Causal review

Check:

Does every impact have an intermediate chain?
Are correlation and causation confused?
Can historical documents override structured facts?
Are contributing causes labelled properly?
25.2 Adversarial model scenarios
Scenario A: No impact

Supplier outage occurs, but sufficient inventory exists for the entire horizon.

Expected:

Plain Text
Affected supply: Yes
Operational shortage: No
SLA breaches: 0
Revenue at risk: ₹0
Scenario B: No feasible intervention
No transferable inventory
No approved alternate supplier
PO cannot be expedited
Production rescheduling cannot resolve shortage

Expected:

Plain Text
NO_FEASIBLE_INTERVENTION
Scenario C: Insufficient data

No valid inventory snapshot exists.

Expected:

Plain Text
INSUFFICIENT_DATA

Not:

Plain Text
0 inventory
Scenario D: Partial fulfilment

Only half the customer quantity can be delivered on time.

Expected:

Partial late quantity
Proportional revenue at risk
One breached order
Scenario E: Cheaper but worse intervention

An intervention has the lowest cost but more SLA breaches.

Expected:

It does not win under MINIMIZE_SLA_BREACHES.
Scenario F: Rescheduling externality

Moving one production order earlier delays another high-value order.

Expected:

Both benefit and harm are calculated.
Scenario G: Late-arriving correction

Inventory correction arrives after scenario completion.

Expected:

Original scenario remains unchanged.
A new scenario version may use the correction.
Scenario H: Identical candidates

Two candidates have identical metrics.

Expected:

Tie is reported.
Stable tie-breaker is used only if one recommendation is required.
25.3 Model consistency checks
Conservation of inventory

For every component and scenario:

EndingInventory=StartingInventory+Receipts+TransfersIn−Consumption−TransfersOutEndingInventory = StartingInventory + Receipts + TransfersIn - Consumption - TransfersOutEndingInventory=StartingInventory+Receipts+TransfersIn−Consumption−TransfersOut

Any unexplained difference is a failure.

Conservation of production
CompletedQuantity≤PlannedQuantityCompletedQuantity \le PlannedQuantityCompletedQuantity≤PlannedQuantity
Allocation conservation
∑AllocatedQuantity≤EligibleAvailableQuantity\sum AllocatedQuantity \le EligibleAvailableQuantity∑AllocatedQuantity≤EligibleAvailableQuantity
Revenue-at-risk bound
0≤RevenueAtRisk≤TotalOpenOrderRevenue0 \le RevenueAtRisk \le TotalOpenOrderRevenue0≤RevenueAtRisk≤TotalOpenOrderRevenue
Intervention-cost bound
InterventionCost≥0InterventionCost \ge 0InterventionCost≥0
Time ordering
ProjectedCompletion≥ProjectedStartProjectedCompletion \ge ProjectedStartProjectedCompletion≥ProjectedStart ProjectedDelivery≥ProjectedProductAvailabilityProjectedDelivery \ge ProjectedProductAvailabilityProjectedDelivery≥ProjectedProductAvailability
Deliverables
Plain Text
docs/domain/domain-review-report.md
docs/domain/adversarial-scenarios.md
docs/domain/invariant-catalogue.md
