# Phase 7 End-to-End Audit Report

## Scope

Phase 7 intervention optimization, sub-phases A–U.

## What Was Wrong Before

- `src/backend/chronosdb/optimization/` was largely a mock tree.
- All ten adversarial tests were empty `pass` bodies.
- The benchmark evaluator returned hardcoded `1.0` and `0.98`.
- Normalization iterated candidate × metric and produced a Cartesian product.
- Utility scoring double-counted cost and delay.
- Sensitivity analysis ignored supplied weights.
- Ledger paths used `/home/user/...`, UUIDs, and wall-clock timestamps.
- `OptimizationService` hardcoded `HYBRID` and `0.91`.
- The previous audit report claimed completion without executable evidence.

## What Is Implemented Now

| Phase | Evidence |
|---|---|
| 7A | Live Phase 6 bridge and handoff validator |
| 7B | Typed deterministic contracts and hashing |
| 7C | Six objectives, validated weight vectors |
| 7D | Strict YAML registry covering seven categories |
| 7E | Hard/soft feasibility with explicit applicability |
| 7F | Metrics extracted from Phase 6 and operational state |
| 7G | One min-max normalization pass over feasible candidates |
| 7H | Positive oriented utility components, no double subtraction |
| 7I/7J | Pareto and dominance over feasible candidates |
| 7K | Deterministic tie-break policy and rationale |
| 7L | Explicit ±20% revenue/SLA/cost/delay variations |
| 7M | Audit reference, weights, hashes, policies |
| 7N | Deterministic JSONL ledger with all seven required record types |
| 7O | Frozen six-candidate golden fixture |
| 7P | Five benchmark metrics computed from data |
| 7Q | 500ms budget measurement |
| 7R | 20 real tests including all ten adversarial cases |
| 7S | Structured events |
| 7T | Automated domain/optimization/audit/judge review gate, wired into engine |
| 7U | Validated Phase 8 handoff package |

## Verified Results

Command: `.venv/Scripts/python -m pytest tests/optimization -q`

Result: `20 passed`.

Command: `.venv/Scripts/python scripts/validate_phase7.py`

Result: `Phase 7 validation: PASS`, including:

- Golden recommendation `HYBRID`, utility `0.889`, cost ₹132,000
- Live recommendation `EXPEDITE`, cost ₹3,650, ₹1,600,000 revenue protected
- Golden benchmark 100% on feasibility, utility, constraints, Pareto,
  and recommendation
- Reproducible golden result hash
  `26b6524754ac5cd289371788fb75885db418d3023862789de1405d884a0f338e`
- Ledger append of all seven record types, deterministic run IDs, and per-record hashes
- Phase 8 handoff contract valid
- Candidate-only performance check within 500ms

Command: `.venv/Scripts/python -m pytest -q`

Result: `264 passed, 1 skipped`. The skipped test is the pre-existing optional
Docker/Db2 integration check.

The API optimization endpoint is warmed at service construction so a request
reuses the frozen Phase 6 baseline. It completes under the existing 1-second API
load assertion; the Phase 7 validator separately measures the candidate-only
pipeline.

## Deliberate Distinction: Golden vs Live

The specification's golden expectation is `HYBRID` at ₹132,000. The frozen
synthetic fixture meets that expectation.

The live Phase 6 hybrid costs ₹852,400. Under the live ₹200,000 hard cost
constraint it is infeasible. The live engine therefore recommends `EXPEDITE`,
which costs ₹3,650, protects ₹1.6M, and avoids both SLA breaches. The engine does
not special-case `HYBRID` to make a document pass.

## Limitations

1. Docker is unavailable (`docker: command not found`), so Db2 persistence is
   not verified. The JSONL ledger is the verified persistence path.
2. There is no independent real-world optimization benchmark; accuracy is against
   a frozen fixture and Phase 6 consistency.
3. Performance was measured on one machine with a single candidate-only run, not
   as a production p95.
4. Phase 7T is an automated review gate, not external human sign-off.
5. The golden fixture contains a sixth candidate (`RESCHEDULE`) because Phase 7A
   requires the Phase 6 reschedule handoff; the specification's five-candidate
   list omitted it.

## Status

Phase 7 is implemented and verified to the limits above. It is not claimed that
Db2 persistence or an external human review has been exercised.
