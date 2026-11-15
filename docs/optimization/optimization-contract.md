# Phase 7B: Optimization Contract

## Canonical Signature

```python
OptimizationEngine(root=Path).run() -> OptimizationResult
OptimizationEngine(root=Path).optimize_candidates(
    candidates: Sequence[CandidateMetrics],
    *,
    scenario_id: str,
    baseline_state_hash: str,
    rule_set_version: str,
    run_id: str | None = None,
    ledger: OptimizationLedger | None = None,
) -> OptimizationResult
```

`run()` is the live path: it reconstructs the Phase 5 state, executes the six
Phase 6 candidates, and passes their metrics into the same pipeline used by
`optimize_candidates()`.

## Deterministic Inputs

- Phase 6 `CounterfactualResult` values and hashes
- Versioned constraint registry (`config/constraints/registry.yaml`)
- Explicit `OptimizationObjective` weights
- `SCORING_POLICY_VERSION`, `TIE_BREAK_POLICY`, and risk policy version
- Candidate IDs and simulation hashes

## Must Not Depend On

- LLM ranking or narration
- Wall-clock time, UUIDs, or database insertion order
- UI order or request order
- Random tie-breaking
- Metrics that were not recorded by Phase 6

## Output Contract

`OptimizationResult` contains:

| Field | Meaning |
|---|---|
| `candidates` | Raw, unmodified candidate metrics |
| `feasibility` | Every constraint result plus `FEASIBLE`, `CONDITIONALLY_FEASIBLE`, or `INFEASIBLE` |
| `normalized` | Feasible-candidate min-max scores, oriented so 1.0 is better |
| `utilities` | Weighted utility and rank |
| `pareto` | Pareto status for feasible candidates; `NOT_EVALUATED` for infeasible candidates |
| `recommendation` | Winner, score, rationale, ranking, and selected simulation hash |
| `sensitivity` | Explicit ±20% weight variations and winner changes |
| `provenance` | Weights, constraints, rule versions, simulation hashes, tie-break policy, explanation |
| `result_hash` | SHA-256 of the deterministic decision package |

## Determinism

The same Phase 6 hashes, constraint version, objective, and engine version
produce the same recommendation and `result_hash`. Runtime is measured and
reported but excluded from the hash. This is exercised by
`tests/optimization/test_optimization_adversarial.py` and
`scripts/validate_phase7.py`.
