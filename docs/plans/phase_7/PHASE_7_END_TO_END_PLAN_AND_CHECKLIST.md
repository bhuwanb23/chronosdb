# Phase 7 End-to-End Plan and Checklist

**Goal:** Select the best feasible recovery plan under explicit constraints.
**Deliverable:** `chronosdb-optimization-engine-v1.0.0`.
**Status:** implemented and machine-verified through A–U.

## Sub-Phases

| Phase | Implementation | Status |
|---|---|---|
| 7A | `optimization/phase6.py` live handoff validation | PASS |
| 7B | `optimization/contracts.py` | PASS |
| 7C | objective and weight validation | PASS |
| 7D | strict `config/constraints/registry.yaml` | PASS |
| 7E | `optimization/feasibility.py` | PASS |
| 7F | `optimization/metrics.py` | PASS |
| 7G | `optimization/normalization.py` | PASS |
| 7H | `optimization/utility.py` | PASS |
| 7I | `optimization/pareto.py` | PASS |
| 7J | `optimization/dominance.py` | PASS |
| 7K | `optimization/recommendation.py` | PASS |
| 7L | `optimization/sensitivity.py` | PASS |
| 7M | `optimization/provenance.py` | PASS |
| 7N | deterministic JSONL `optimization/ledger.py` | PASS (JSONL only; Db2 unavailable) |
| 7O | frozen `data/golden/phase7-optimization.json` | PASS |
| 7P | `optimization/benchmark.py` | PASS (all five metrics 100%) |
| 7Q | `optimization/performance.py` | PASS (single-run budget check) |
| 7R | real adversarial test suite | PASS (20 tests) |
| 7S | `optimization/observability.py` | PASS |
| 7T | automated `optimization/review.py` gate | PASS (not external human sign-off) |
| 7U | `optimization/handoff.py` | PASS |

## Final Gate

- [x] Phase 6 candidates come from the canonical engine.
- [x] Hard-constraint violations are rejected.
- [x] Utilities use normalized, oriented metrics without double negatives.
- [x] Pareto analysis is restricted to feasible candidates.
- [x] Recommendation and result hash are reproducible.
- [x] Provenance contains simulation hashes, weights, constraints, and policy versions.
- [x] Ledger is deterministic and free of UUIDs and wall-clock timestamps.
- [x] Golden benchmark passes: feasibility 100%, utility 100%, constraints 100%,
  Pareto 100%, recommendation 100%.
- [x] Phase 8 handoff contract validates.
- [ ] Db2 optimization-run persistence verified (blocked: Db2 unavailable).
- [x] Full test-suite regression run recorded separately.

## Key Evidence

- `artifacts/phase-7/phase7-validation-report.json`
- `artifacts/phase-7/phase7-golden-result.json`
- `artifacts/phase-7/phase7-live-result.json`
- `artifacts/phase-7/phase7-benchmark.json`
- `artifacts/phase-7/phase7-phase8-handoff.json`
- `docs/optimization/phase-7-implementation.md`

## Live-vs-Specification Note

The synthetic golden fixture expects `HYBRID` at ₹132,000 and does so. The live
Phase 6 hybrid costs ₹852,400 and violates the real ₹200,000 budget, so the live
winner is `EXPEDITE`. This is a data/specification distinction, not a hidden
override.
