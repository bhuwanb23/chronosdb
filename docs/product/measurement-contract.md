# Measurement Contract

These measures are frozen before domain implementation. They are planned
targets, not current performance or accuracy claims.

## Correctness

### Impact precision

`correctly predicted affected entities / all predicted affected entities`

Target: at least 95%; the golden scenario target is 100%.

### Impact recall

`correctly predicted affected entities / all actually affected entities`

Target: at least 95%; the golden scenario target is 100%.

### Numerical fidelity

`verified displayed numerical claims / all displayed numerical claims`

Target: 100%.

### Feasibility accuracy

`correct candidate classifications / all candidate classifications`

Target: 100% for the golden scenario and at least 98% for the benchmark set.

### Recommendation agreement

`scenarios matching an accepted benchmark optimum / evaluated scenarios`

Target: at least 90%. Tied or Pareto-equivalent valid plans must count as
accepted outcomes.

### Evidence coverage

`verifiable claims linked to evidence / all verifiable claims`

Target: 100%.

## AI and retrieval

When an AI layer exists:

- valid structured scenario rate: at least 95%;
- invalid-input rejection: 100%;
- unknown-supplier rejection: 100%;
- unsupported-objective rejection: 100%;
- invented-identifier acceptance: 0%;
- retrieval Recall@5: at least 0.85;
- retrieval Precision@5: at least 0.75;
- retrieval MRR: at least 0.80;
- structured-filter compliance: 100%;
- unauthorized-document retrieval: 0%.

These metrics must be measured against a frozen corpus and prompt/test set.

## Performance

Report median, p95, maximum, and error rate for:

- scenario validation;
- baseline impact;
- one intervention;
- five-candidate comparison;
- evidence retrieval;
- full deterministic response;
- historical replay.

Every report must include dataset size, hardware, Db2 version, software
versions, and warm versus cold execution.

## Human understanding

With at least five reviewers, measure whether a reviewer can:

- identify affected orders in under 30 seconds;
- identify the recommendation in under 15 seconds;
- locate supporting evidence in under 30 seconds;
- explain the main trade-off after one viewing.

Also record understanding confidence from 1–5 and the evaluation limitations.

## Measurement rules

1. Synthetic data must be labelled as synthetic.
2. Failed cases must remain in denominators unless the metric definition
   explicitly says otherwise.
3. Targets cannot be converted into claims until the test artifact exists.
4. Every result records the rule version and source dataset.
