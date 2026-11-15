# Phase 6 Handoff Review

Phase 7 accepts candidates only through `Phase6CandidateBuilder`, which calls
the canonical `Phase6Engine` and validates the handoff before optimization.

## Required Candidates

- Do Nothing (the Phase 6 baseline)
- Transfer
- Expedition
- Alternate Supplier
- Reschedule
- Hybrid

## Live Handoff Metrics (frozen Phase 6 fixture)

| Candidate | Revenue protected | Breaches avoided | Max delay | Recovery cost |
|---|---:|---:|---:|---:|
| Do Nothing | ₹0 | 0 | 288 h | ₹0 |
| Transfer | ₹800,000 | 1 | 216 h | ₹32,800 |
| Expedition | ₹1,600,000 | 2 | 0 h | ₹3,650 |
| Alternate Supplier | ₹400,000 | 0 | 264 h | ₹813,000 |
| Reschedule | ₹0 | 0 | 360 h | ₹12,000 |
| Hybrid | ₹800,000 | 1 | 216 h | ₹852,400 |

## Validation Checks

- At least two candidates and a `DO_NOTHING` baseline
- Every candidate has source `PHASE6`
- Unique candidate IDs and simulation hashes
- Consistent baseline result hash and rule-set version
- All required metrics finite
- Phase 6 status `COMPLETED`
- No duplicate or conflicting overlay IDs

The handoff is exercised live in
`tests/optimization/test_optimization_adversarial.py` and
`scripts/validate_phase7.py`.

## Important Consequence

Under the live constraints, `EXPEDITE` is the feasible winner. The live hybrid
is rejected by `max_recovery_cost`; it is not the same plan as the synthetic
golden hybrid. See `docs/optimization/phase-7-implementation.md`.
