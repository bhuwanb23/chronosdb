# Phase 2 Completion Report

## Scope

Phase 2A–2V is complete as a domain, temporal, causal, formula, ground-truth,
and validation specification. Physical Db2 design and executable behavior remain
later implementation work.

## Locked decisions

- Primary scenario: `SUPPLIER_OUTAGE`.
- Bounded context: simplified manufacturing supply-chain planning.
- Primary units: `EA` for the golden component/product quantities.
- MVP currency: INR.
- Canonical time: UTC; display zone: Asia/Kolkata.
- Missing critical data: `INSUFFICIENT_DATA`.
- Hard constraints are filtered before ranking.
- Operational state is immutable during counterfactual evaluation.
- Corrected golden scenario uses Chennai on-hand 700 and transferable 400 MCU
  units.

## Quality scorecard

| Measure | Result |
|---|---|
| Domain concepts formally modelled | 100% |
| Numerical outputs with frozen formulas | 100% for the defined MVP outputs |
| Golden-scenario causal coverage | 100% |
| Time-dependent entities with boundary rules | 100% |
| Documented entities with invariants | 100% |
| Independent golden-output agreement | 100% |
| Priority 0 material ambiguity | 0 unresolved in Phase 2 |
| Priority 0 traceability | 100% |

These are specification and manual-validation results, not runtime benchmark
claims.

## Golden-scenario ground truth

- No-disruption breached orders: 0.
- Do-nothing breached orders: 2.
- Do-nothing revenue at risk: INR 1,600,000.
- Transfer-only breached orders: 1.
- Alternate-only breached orders: 2.
- Hybrid intervention cost: INR 132,000.
- Hybrid breached orders: 0.
- Hybrid revenue at risk: INR 0.
- Hybrid revenue protected: INR 1,600,000.
- Expected recommendation: `INT-HYBRID-400`.

Two independent manual calculation paths agree on all listed outputs. The
original 200-unit transfer variant is explicitly rejected and cannot be used
as benchmark ground truth.

## Phase 3 handoff

Phase 3 must generate data without inventing rules. Required inputs are:

- entity catalogue, attributes, relationships, and cardinalities;
- lifecycle states and effective-time rules;
- units, currency, precision, costs, revenue, capacity, and lead times;
- outage behavior, inventory propagation, BOM requirements, scheduling,
  fulfilment, SLA, and intervention overlays;
- formula and objective versions;
- uncertainty states and evidence/provenance requirements;
- domain invariants, rejection codes, tests, and adversarial cases;
- corrected golden records and expected outputs.

Phase 3 must produce a data-generation specification, reproducible synthetic
generator, seed dataset, data dictionary, validator, golden dataset, benchmark
scenarios, ground-truth outcomes, statistics, and reproducibility report.

## Final gate

**Phase 2 specification gate: PASS.** An independent engineer can use the
domain rules and corrected golden records to calculate the primary impact and
recommendation without inventing business behavior. Implementation correctness
is intentionally deferred to Phases 3–7.
