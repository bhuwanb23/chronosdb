# Phase 6 Validation Report

## Verdict

**PASS after remediation.**

The Phase 6 deliverables that existed at the start of this audit were not a
working counterfactual engine. The test suite passed, but the tests exercised
mock implementations:

- `phase6b_contract.simulate()` raised `NotImplementedError`.
- `phase6l_execution_engine` hardcoded `engine_version: 5.3.2` and did not run
  the Phase 5 engine.
- `phase6f`–`phase6k` returned fixed quantities, dates, costs, and deltas.
- `phase6q` golden expectations were arbitrary constants that did not match a
  simulation.
- `phase6t` adversarial fixtures always returned `passed: True`.
- No Phase 6 artifacts, golden overlays, or Phase 6 validator existed.

A real engine was added at `src/chronosdb/simulation/counterfactual.py`. It
rebuilds the frozen Phase 5 state, applies virtual overlay records to a copy,
and re-runs `calculate_impact` with the unchanged disruption, horizon, and rule
set. Phase 5 allocation, scheduling, and financial logic is not reimplemented.

## Verification evidence

| Check | Result |
|---|---|
| Phase 5 baseline handoff hash | `e200e191f0fa5f6ca61b5057205076fdd8913a9adf490560556c43812d38bc3b` |
| Phase 5 baseline state hash | `47e178713708fe62e1eee1c68edbaa448fb88a519c418221a6fa31f96142b286` |
| Golden interventions | 5 / 5 executed through Phase 5 |
| 100-run transfer determinism | 1 unique business output |
| 20-scenario × 10-rerun benchmark | 200 stable outputs |
| Adversarial fixtures | 10 / 10 rejected with typed errors |
| Baseline record mutation | none |
| Persistence | 5 append-only ledger records |
| P95 full hybrid scenario | within 2,500 ms target |

### Golden outcomes

| Scenario | Revenue risk | Revenue protected | Breaches avoided | Max-delay reduction | Cost |
|---|---:|---:|---:|---:|---:|
| Transfer 400 units | 800,000 | 800,000 | 1 | 72 h | 32,800 |
| Expedite PO-2208 by 5 days | 0 | 1,600,000 | 2 | 288 h | 3,650 |
| Alternate supplier, 300 units | 1,200,000 | 400,000 | 0 | 24 h | 813,000 |
| Reschedule MO-0882 to CRITICAL | 1,600,000 | 0 | 0 | -72 h | 12,000 |
| Hybrid transfer + supplier + reschedule | 800,000 | 800,000 | 1 | 72 h | 852,400 |

The reschedule-only result is intentionally negative on delay and net benefit:
it is a valid simulation outcome, not a gate failure. Phase 7 must rank it below
the other candidates rather than Phase 6 hiding an unattractive result.

## Adversarial coverage

The validator now rejects negative transfer quantity, transfer above stock,
safety-stock violation, unknown supplier, missing/expired agreement, impossible
purchase order, invalid priority, broken action, duplicate overlay, and
conflicting overlays. Every case raises `SimulationValidationError`; no
simulation executes and the baseline remains unchanged.

## Artifacts

- `artifacts/phase-6/validation-report.json`
- `artifacts/phase-6/golden-results.json`
- `artifacts/phase-6/determinism-report.json`
- `artifacts/phase-6/performance-report.json`
- `artifacts/phase-6/adversarial-report.json`
- `artifacts/phase-6/simulation-ledger.jsonl`
- `artifacts/phase-6/phase-7-handoff.json`

## Commands run

```bash
.venv/Scripts/python -m pytest tests/simulation -q
.venv/Scripts/python -m pytest -q
.venv/Scripts/python scripts/validate_phase5.py
.venv/Scripts/python scripts/validate_phase6.py
.venv/Scripts/python scripts/validate_phase15.py
```

## Limitations

- Validation uses the frozen golden scenario. There is no independent
  real-world benchmark dataset, so “fidelity” means internal consistency with
  the locked Phase 5 baseline, not predictive accuracy.
- The ledger is an append-only JSONL artifact, not a Db2-backed production
  table. Docker and Db2 are unavailable in this environment.
- The original `phase6a`–`phase6w` modules remain in the tree as legacy
  sub-phase scaffolding. The canonical runtime path is
  `simulation.counterfactual.Phase6Engine`; consumers must not use the legacy
  mock modules.
