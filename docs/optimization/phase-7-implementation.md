# Phase 7 Implementation

## Canonical Modules

| Phase | Module |
|---|---|
| 7A | `src/backend/chronosdb/optimization/phase6.py` |
| 7B | `contracts.py` |
| 7C | `contracts.py` (`OptimizationObjective`, `WeightVector`) |
| 7D | `constraints.py`, `config/constraints/registry.yaml` |
| 7E | `feasibility.py` |
| 7F | `metrics.py` |
| 7G | `normalization.py` |
| 7H | `utility.py` |
| 7I | `pareto.py` |
| 7J | `dominance.py` |
| 7K | `recommendation.py` |
| 7L | `sensitivity.py` |
| 7M | `provenance.py` |
| 7N | `ledger.py` |
| 7O | `golden.py`, `data/golden/phase7-optimization.json` |
| 7P | `benchmark.py` |
| 7Q | `performance.py` |
| 7R | `tests/optimization/test_optimization_adversarial.py` |
| 7S | `observability.py` |
| 7T | `review.py` |
| 7U | `handoff.py` |

The engine is `engine.py`. The API service
(`src/backend/chronosdb/services/optimization_service.py`) now calls it instead
of returning a hardcoded `HYBRID` / `0.91`. The service warms the immutable
Phase 6 baseline at construction and reuses it across requests; candidate
execution is still fresh and deterministic.

## Scoring

Normalization is performed once over the feasible set:

- benefits: `(value - min) / (max - min)`
- costs: `(max - value) / (max - min)`

All five normalized terms are oriented so 1.0 is better:

```
U = 0.40 × revenue_protected
  + 0.30 × breaches_avoided
  + 0.15 × cost_efficiency
  + 0.10 × delay_reduction
  + 0.05 × risk_avoidance
```

This is algebraically the Phase 7 formula with cost and delay signs moved into
normalization. Cost is **not** subtracted twice. If a metric is identical across
every feasible candidate, it contributes 0.0 to everyone and cannot break a tie.

## Tie-Breaking

1. Higher utility
2. Higher revenue protected
3. More SLA breaches avoided
4. Greater delay reduction
5. Lower recovery cost
6. Lower supplier risk
7. Lexicographic candidate ID

No random or insertion-order tie-break exists.

## Pareto Semantics

Pareto is evaluated over feasible candidates only. Infeasible candidates receive
`NOT_EVALUATED`; their raw metrics are still visible. A plan that looks
attractive only because it violates a constraint cannot dominate a feasible plan.

## Provenance and Ledger

`ProvenanceTracker` builds an `audit:<hash>` reference from candidate IDs,
simulation hashes, constraint version, rule versions, objective, selected
candidate, and sensitivity outcome. `DecisionProvenance` records weights,
constraint results, metric values, simulation hashes, and the scoring/tie-break
policy versions.

The JSONL ledger uses project-relative or injected paths, deterministic run IDs,
and `created_at: "deterministic"`. Each run appends the seven required record
types: `OPTIMIZATION_RUN`, `INPUT`, `CANDIDATE_SCORE`, `CONSTRAINT_RESULT`,
`PARETO_RESULT`, `RECOMMENDATION`, and `SENSITIVITY_RESULT`. Every row carries a
SHA-256 `record_hash`. It contains no UUIDs and no wall-clock time.

## Verification

```bash
.venv/Scripts/python -m pytest tests/optimization -q
.venv/Scripts/python scripts/validate_phase7.py
```

The validator runs the frozen golden fixture, the live Phase 6 handoff, ledger
append, benchmark, deterministic replay, and a 500ms performance budget check.
It writes evidence to `artifacts/phase-7/`.

Latest verified results:

- Optimization tests: 20 passed
- Golden recommendation: `HYBRID`, utility `0.889`, ₹132,000
- Live recommendation: `EXPEDITE`, ₹3,650, ₹1.6M protected, 2 breaches avoided
- Golden benchmark: all five metrics 100%
- Candidate-only measured runtime: about 10ms on this machine (single run, not a
  statistical p95)
- Full suite: 264 passed, 1 skipped (Docker/Db2 integration)

## Known Limitations

- Docker and Db2 are unavailable here. JSONL persistence is verified; Db2
  optimization-run persistence is not.
- No independent real-world optimization benchmark exists. Accuracy is measured
  against a frozen synthetic fixture and Phase 6 consistency.
- The live constraints make the ₹852,400 hybrid infeasible. The specification's
  `HYBRID` expectation applies to the synthetic golden fixture, not the live
  scenario. The live engine recommends `EXPEDITE`; forcing `HYBRID` would require
  changing the real cost constraint or inventing a cheaper hybrid simulation.
- The review gate is automated and auditable. It does not claim an external
  human sign-off.
