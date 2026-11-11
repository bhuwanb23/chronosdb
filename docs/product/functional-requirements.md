# Functional Requirements

`SHALL` is mandatory for the deterministic vertical slice. `SHOULD` is
important but may follow after the core slice. Every requirement is intended to
map to a future automated or acceptance test.

## Scenario management

- **FR-SCN-001:** The system SHALL create a supplier-outage scenario from
  structured input.
- **FR-SCN-002:** The system SHALL assign a unique scenario identifier.
- **FR-SCN-003:** The system SHALL store creation time, state reference,
  objective, constraints, and rule version.
- **FR-SCN-004:** The system SHALL validate the supplier against active records.
- **FR-SCN-005:** The system SHALL reject missing or non-positive duration.
- **FR-SCN-006:** The system SHALL reject an unsupported objective or invalid
  constraint.
- **FR-SCN-007:** The system SHALL preserve the exact input after execution
  begins.
- **FR-SCN-008:** The system SHOULD allow an existing scenario to be duplicated
  into a new scenario.

## Impact analysis

- **FR-IMP-001:** The system SHALL identify components supplied by the
  disrupted supplier.
- **FR-IMP-002:** The system SHALL identify affected replenishments and project
  available inventory.
- **FR-IMP-003:** The system SHALL calculate shortage date and quantity for
  each affected component.
- **FR-IMP-004:** The system SHALL traverse bill-of-material dependencies.
- **FR-IMP-005:** The system SHALL identify affected production orders and
  projected delay.
- **FR-IMP-006:** The system SHALL identify affected customer orders and
  projected delivery.
- **FR-IMP-007:** The system SHALL classify projected SLA status.
- **FR-IMP-008:** The system SHALL calculate revenue at risk using a documented
  rule.
- **FR-IMP-009:** The system SHALL preserve intermediate values and produce a
  do-nothing baseline.

## Interventions and simulation

- **FR-INT-001:** The system SHALL evaluate do nothing, inventory transfer,
  shipment expedition, approved alternate supplier, and production
  rescheduling.
- **FR-INT-002:** The system SHOULD evaluate a hybrid intervention.
- **FR-INT-003:** The system SHALL preserve infeasible candidates and rejection
  reasons.
- **FR-INT-004:** The system SHALL enforce inventory, safety-stock, supplier
  approval, capacity, timing, and budget constraints.
- **FR-INT-005:** The system SHALL calculate intervention cost from documented
  cost components.
- **FR-SIM-001:** Each feasible candidate SHALL run against the same immutable
  baseline.
- **FR-SIM-002:** Simulation SHALL NOT mutate operational baseline records.
- **FR-SIM-003:** The system SHALL assign a simulation-run identifier and rule
  version.
- **FR-SIM-004:** The system SHALL record warnings and errors.
- **FR-SIM-005:** Repeating the same state, input, and rule version SHALL
  produce the same result.

## Optimization and recommendation

- **FR-OPT-001:** The system SHALL rank only feasible candidates.
- **FR-OPT-002:** Ranking SHALL use the selected objective and visible
  constraints.
- **FR-OPT-003:** The system SHALL expose the objective, weights, and
  constraints used.
- **FR-OPT-004:** The system SHALL identify ties.
- **FR-OPT-005:** The system SHALL return `NO_FEASIBLE_INTERVENTION` when
  appropriate.
- **FR-OPT-006:** The system SHALL explain the selected intervention and its
  primary trade-off.

## Evidence and explanation

- **FR-EVD-001:** Every major numerical claim SHALL link to a scenario or
  simulation run.
- **FR-EVD-002:** Major calculations SHALL identify source records and rule
  version.
- **FR-EVD-003:** Retrieved documents SHALL retain source, version, and chunk
  identity.
- **FR-EVD-004:** The system SHALL distinguish Db2 facts, derived values,
  controlled documents, and generated explanation.
- **FR-EVD-005:** The system SHALL indicate unavailable evidence and SHALL NOT
  fabricate an evidence link.
- **FR-EXP-001:** The system SHALL explain baseline impact, recommendation,
  trade-offs, and remaining risks.
- **FR-EXP-002:** Any future generated numerical statement SHALL be verified
  against structured output.
- **FR-EXP-003:** The system SHALL provide a deterministic summary when an LLM
  is disabled or unavailable.

## Audit

- **FR-AUD-001:** The system SHALL record scenario creation, simulation runs,
  candidate feasibility, recommendation, and verification results.
- **FR-AUD-002:** The system SHALL preserve the original scenario and decision
  history.
- **FR-AUD-003:** A completed decision SHALL be replayable without changing its
  original result.
- **FR-AUD-004:** The normal application role SHALL NOT modify historical audit
  records.

## Traceability

The requirements above trace to `UN-001` through `UN-010` in
[`user-needs.md`](user-needs.md) and to `UC-001` through `UC-009` in
[`use-case-catalogue.md`](use-case-catalogue.md). Future implementation phases
must add concrete test IDs before marking requirements complete.
