15. Phase 1M: Success metrics and evaluation contract
Goal

Define metrics before implementation so later benchmarks cannot be manipulated around observed results.

15.1 Product-correctness metrics
Impact precision
Impact Precision=correctly predicted affected entitiesall predicted affected entities\text{Impact Precision} = \frac{\text{correctly predicted affected entities}} {\text{all predicted affected entities}}

## Target:

≥ 95%

Impact recall
Impact Recall=correctly predicted affected entitiesall actually affected entities\text{Impact Recall} = \frac{\text{correctly predicted affected entities}} {\text{all actually affected entities}}

## Target:

≥ 95%


For the golden deterministic scenario, both should reach 100%.

15.2 Numerical fidelity
Numerical Fidelity=displayed numerical claims matching structured outputsall displayed numerical claims\text{Numerical Fidelity} = \frac{\text{displayed numerical claims matching structured outputs}} {\text{all displayed numerical claims}}

## Target:

100%

15.3 Intervention feasibility
Feasibility Accuracy=correct candidate feasibility classificationsall candidate classifications\text{Feasibility Accuracy} = \frac{\text{correct candidate feasibility classifications}} {\text{all candidate classifications}}

## Target:

100% for golden scenario
≥ 98% for benchmark suite

15.4 Recommendation agreement
Optimal Plan Agreement=scenarios where selected plan matches benchmark optimumevaluated benchmark scenarios\text{Optimal Plan Agreement} = \frac{\text{scenarios where selected plan matches benchmark optimum}} {\text{evaluated benchmark scenarios}}

## Target:

≥ 90%


If multiple plans are tied or Pareto-efficient, the benchmark must recognize all valid answers.

15.5 Evidence coverage
Evidence Coverage=verifiable claims linked to evidenceall verifiable claims\text{Evidence Coverage} = \frac{\text{verifiable claims linked to evidence}} {\text{all verifiable claims}}

## Target:

100%

15.6 AI parsing metrics
Valid structured scenario rate: at least 95%
Invalid-input rejection: 100%
Unknown supplier rejection: 100%
Unsupported objective rejection: 100%
Invented identifier acceptance: 0%
15.7 Retrieval metrics

## Targets for the frozen evidence corpus:

Recall@5: at least 0.85
Precision@5: at least 0.75
Mean Reciprocal Rank: at least 0.80
Structured-filter compliance: 100%
Unauthorized-document retrieval: 0%
15.8 Performance metrics

## Report:

Median
p95
Maximum
Error rate
Dataset size
Hardware
Db2 version
Warm versus cold execution

No single latency number should be reported without test conditions.

## 15.9 Human-understanding metrics

## For a small evaluation with at least five reviewers, measure:

Can identify affected orders in under 30 seconds
Can identify recommended intervention in under 15 seconds
Can locate supporting evidence in under 30 seconds
Can explain the main trade-off after one viewing
Confidence in understanding, rated 1–5

These are usability measurements, not claims about commercial validation.

Deliverable
docs/product/measurement-contract.md

