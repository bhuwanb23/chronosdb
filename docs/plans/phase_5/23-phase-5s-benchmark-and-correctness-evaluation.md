23. Phase 5S: Benchmark and Correctness Evaluation
Goal

Measure engine correctness against the frozen Phase 4 ground truth.

Evaluation partitions
Development

Visible during implementation.

Validation

Used to tune implementation details without changing business rules.

Test

Frozen and evaluated only after the engine is ready.

Adversarial

Used to verify correct failure behavior.

Correctness metrics
Affected-entity precision
Precision=CorrectlyPredictedAffectedEntitiesAllPredictedAffectedEntitiesPrecision = \frac{CorrectlyPredictedAffectedEntities} {AllPredictedAffectedEntities}Precision=AllPredictedAffectedEntitiesCorrectlyPredictedAffectedEntities​
Affected-entity recall
Recall=CorrectlyPredictedAffectedEntitiesAllGroundTruthAffectedEntitiesRecall = \frac{CorrectlyPredictedAffectedEntities} {AllGroundTruthAffectedEntities}Recall=AllGroundTruthAffectedEntitiesCorrectlyPredictedAffectedEntities​

Calculate independently for:

Purchase orders
Components
Production orders
Customer orders
Numerical exact-match rate
ExactMatch=NumericalFieldsMatchingGroundTruthAllEvaluatedNumericalFieldsExactMatch = \frac{NumericalFieldsMatchingGroundTruth} {AllEvaluatedNumericalFields}ExactMatch=AllEvaluatedNumericalFieldsNumericalFieldsMatchingGroundTruth​

For deterministic monetary and quantity outputs:

Plain Text
Target: 100%
Timestamp accuracy

For exact deterministic scenarios:

Plain Text
Target: Exact timestamp match

Do not hide boundary errors behind wide tolerances.

SLA classification accuracy
SLAAccuracy=CorrectSLAClassificationsAllEvaluatedOrderLinesSLAAccuracy = \frac{CorrectSLAClassifications} {AllEvaluatedOrderLines}SLAAccuracy=AllEvaluatedOrderLinesCorrectSLAClassifications​

Target:

Plain Text
100% for supported, complete-data scenarios
Revenue-at-risk fidelity
FinancialFidelity=CorrectRevenueAtRiskValuesAllScenariosWithDefinedGroundTruthFinancialFidelity = \frac{CorrectRevenueAtRiskValues} {AllScenariosWithDefinedGroundTruth}FinancialFidelity=AllScenariosWithDefinedGroundTruthCorrectRevenueAtRiskValues​

Target:

Plain Text
100%
Causal-trace edge precision
CausalPrecision=CorrectPredictedCausalEdgesAllPredictedCausalEdgesCausalPrecision = \frac{CorrectPredictedCausalEdges} {AllPredictedCausalEdges}CausalPrecision=AllPredictedCausalEdgesCorrectPredictedCausalEdges​
Causal-trace edge recall
CausalRecall=CorrectPredictedCausalEdgesAllExpectedCausalEdgesCausalRecall = \frac{CorrectPredictedCausalEdges} {AllExpectedCausalEdges}CausalRecall=AllExpectedCausalEdgesCorrectPredictedCausalEdges​

Targets:

Plain Text
Golden: 100% precision and recall
Supported test scenarios: ≥98%

If the ground truth permits equivalent causal representations, normalize paths before comparison.

Data-quality classification accuracy

Target:

Plain Text
100%

for:

Complete
Partial
Insufficient data
Invalid input
Required target table
Metric	Golden	Test suite
Affected PO precision	100%	≥99%
Affected PO recall	100%	≥99%
Component precision	100%	≥99%
Component recall	100%	≥99%
Production-order precision	100%	≥98%
Production-order recall	100%	≥98%
Customer-order precision	100%	≥98%
Customer-order recall	100%	≥98%
SLA classification	100%	100%
Quantity fidelity	100%	100%
Financial fidelity	100%	100%
Feasible complete-data run completion	100%	100%
Data-quality classification	100%	100%

For a deterministic engine, unexplained financial or quantity mismatches should block release rather than be accepted as approximate accuracy.

Deliverables
Plain Text
benchmarks/impact/
artifacts/phase-5/impact-benchmark-results.json
artifacts/phase-5/impact-benchmark-report.md
