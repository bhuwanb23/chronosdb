28. Phase 5 Quality Benchmarks
28.1 Deterministic-result stability
DRS=RunsMatchingExpectedResultHashAllRepeatedRunsDRS = \frac{RunsMatchingExpectedResultHash} {AllRepeatedRuns}DRS=AllRepeatedRunsRunsMatchingExpectedResultHash​

Target:

Plain Text
100%
28.2 Numerical fidelity
NF=NumericalOutputsMatchingGroundTruthAllEvaluatedNumericalOutputsNF = \frac{NumericalOutputsMatchingGroundTruth} {AllEvaluatedNumericalOutputs}NF=AllEvaluatedNumericalOutputsNumericalOutputsMatchingGroundTruth​

Target:

Plain Text
100%
28.3 Causal coverage
CC=KeyImpactOutputsWithCompleteCausalTraceAllKeyImpactOutputsCC = \frac{KeyImpactOutputsWithCompleteCausalTrace} {AllKeyImpactOutputs}CC=AllKeyImpactOutputsKeyImpactOutputsWithCompleteCausalTrace​

Target:

Plain Text
100%
28.4 Provenance coverage
PC=KeyOutputsWithCompleteProvenanceAllKeyOutputsPC = \frac{KeyOutputsWithCompleteProvenance} {AllKeyOutputs}PC=AllKeyOutputsKeyOutputsWithCompleteProvenance​

Target:

Plain Text
100%
28.5 State reconstruction accuracy
SRA=ReconstructedStatesMatchingFrozenStateAllHistoricalStateFixturesSRA = \frac{ReconstructedStatesMatchingFrozenState} {AllHistoricalStateFixtures}SRA=AllHistoricalStateFixturesReconstructedStatesMatchingFrozenState​

Target:

Plain Text
100%
28.6 Impact entity F1
F1=2×Precision×RecallPrecision+RecallF1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}F1=2×Precision+RecallPrecision×Recall​

Target:

Plain Text
Golden: 1.0
Supported test scenarios: ≥0.98
28.7 Failure-classification accuracy
FCA=CorrectErrorOrQualityClassificationsAllFailureFixturesFCA = \frac{CorrectErrorOrQualityClassifications} {AllFailureFixtures}FCA=AllFailureFixturesCorrectErrorOrQualityClassifications​

Target:

Plain Text
100%
28.8 Demo latency

Target:

Plain Text
Demo scenario p95 end-to-end impact calculation: <2 seconds
