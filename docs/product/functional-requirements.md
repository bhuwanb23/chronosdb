# Functional Requirements

`SHALL` is mandatory for the deterministic vertical slice. `SHOULD` is
important but may follow after the core slice. Every requirement is intended to
map to a future automated or acceptance test.

## Scenario management

- **FR-SCN-001:** The system SHALL create a supplier-outage scenario from structured input.
- **FR-SCN-002:** The system SHALL assign a unique scenario identifier.
- **FR-SCN-003:** The system SHALL store the scenario creation timestamp.
- **FR-SCN-004:** The system SHALL validate the supplier against active supplier records.
- **FR-SCN-005:** The system SHALL reject non-positive disruption durations.
- **FR-SCN-006:** The system SHALL store the selected optimization objective.
- **FR-SCN-007:** The system SHALL store all user-defined constraints.
- **FR-SCN-008:** The system SHALL preserve the exact operational-state reference used for the scenario.
- **FR-SCN-009:** The system SHALL NOT silently modify scenario inputs after execution begins.
- **FR-SCN-010:** The system SHALL permit a user to duplicate an existing scenario into a new scenario.

## Impact analysis

- **FR-IMP-001:** The system SHALL determine the components supplied by the disrupted supplier.
- **FR-IMP-002:** The system SHALL determine which expected replenishments are affected.
- **FR-IMP-003:** The system SHALL project available inventory over the simulation horizon.
- **FR-IMP-004:** The system SHALL calculate the earliest shortage date for every affected component.
- **FR-IMP-005:** The system SHALL calculate the projected shortage quantity.
- **FR-IMP-006:** The system SHALL identify products whose bills of material depend on affected components.
- **FR-IMP-007:** The system SHALL identify affected production orders.
- **FR-IMP-008:** The system SHALL calculate projected production-order delay.
- **FR-IMP-009:** The system SHALL identify affected customer orders.
- **FR-IMP-010:** The system SHALL calculate projected customer delivery dates.
- **FR-IMP-011:** The system SHALL classify projected SLA status.
- **FR-IMP-012:** The system SHALL calculate revenue at risk using a documented rule.
- **FR-IMP-013:** The system SHALL preserve intermediate calculation values.
- **FR-IMP-014:** The system SHALL produce a do-nothing baseline for every valid scenario.

## Intervention requirements

- **FR-INT-001:** The system SHALL create a do-nothing candidate.
- **FR-INT-002:** The system SHALL evaluate inventory transfer where transferable stock exists.
- **FR-INT-003:** The system SHALL evaluate expedition of eligible purchase orders.
- **FR-INT-004:** The system SHALL evaluate approved alternate suppliers.
- **FR-INT-005:** The system SHALL evaluate production rescheduling.
- **FR-INT-006:** The system SHOULD evaluate at least one hybrid intervention.
- **FR-INT-007:** The system SHALL preserve infeasible candidates and rejection reasons.
- **FR-INT-008:** The system SHALL detect violations of minimum safety stock.
- **FR-INT-009:** The system SHALL detect violations of the recovery budget.
- **FR-INT-010:** The system SHALL reject unapproved supplier substitution.
- **FR-INT-011:** The system SHALL calculate intervention cost using documented components.

## Simulation requirements

- **FR-SIM-001:** The system SHALL simulate each feasible intervention against the same baseline state.
- **FR-SIM-002:** The system SHALL NOT mutate baseline operational records.
- **FR-SIM-003:** The system SHALL assign a unique simulation-run identifier.
- **FR-SIM-004:** The system SHALL record the calculation-rule version.
- **FR-SIM-005:** The system SHALL record simulation warnings and errors.
- **FR-SIM-006:** The system SHALL produce identical results for the same input state and rule version.
- **FR-SIM-007:** The system SHALL prevent scenarios from contaminating one another.

## Optimization requirements

- **FR-OPT-001:** The system SHALL rank only feasible interventions.
- **FR-OPT-002:** The system SHALL rank candidates according to the selected objective.
- **FR-OPT-003:** The system SHALL expose the objective and weights used.
- **FR-OPT-004:** The system SHALL expose the constraints applied.
- **FR-OPT-005:** The system SHALL identify ties.
- **FR-OPT-006:** The system SHALL return NO_FEASIBLE_INTERVENTION when no candidate satisfies the constraints.
- **FR-OPT-007:** The system SHALL provide a reason for the selected intervention.
- **FR-OPT-008:** The system SHOULD expose Pareto-efficient candidates when objectives conflict.

## Evidence requirements

- **FR-EVD-001:** The system SHALL associate every major numerical claim with a simulation run.
- **FR-EVD-002:** The system SHALL identify the source records used by major calculations.
- **FR-EVD-003:** The system SHALL store the calculation rule version.
- **FR-EVD-004:** The system SHALL retrieve relevant historical incidents.
- **FR-EVD-005:** The system SHALL retrieve relevant operating procedures.
- **FR-EVD-006:** The system SHALL preserve document version and chunk identity for retrieved evidence.
- **FR-EVD-007:** The system SHALL distinguish database facts from retrieved documents.
- **FR-EVD-008:** The system SHALL indicate when supporting evidence is unavailable.
- **FR-EVD-009:** The system SHALL NOT fabricate an evidence link.

## Explanation requirements

- **FR-EXP-001:** The system SHALL explain the do-nothing impact.
- **FR-EXP-002:** The system SHALL explain why the recommended intervention was selected.
- **FR-EXP-003:** The system SHALL explain the primary trade-off.
- **FR-EXP-004:** The system SHALL expose remaining risks.
- **FR-EXP-005:** The system SHALL verify generated numerical statements against structured outputs.
- **FR-EXP-006:** The system SHALL remove or reject unsupported numerical statements.
- **FR-EXP-007:** The system SHALL provide a deterministic summary if the LLM is unavailable.

## Audit requirements

- **FR-AUD-001:** The system SHALL record scenario creation.
- **FR-AUD-002:** The system SHALL record each simulation run.
- **FR-AUD-003:** The system SHALL record candidate feasibility decisions.
- **FR-AUD-004:** The system SHALL record the selected recommendation.
- **FR-AUD-005:** The system SHALL record model calls used for planning or narration.
- **FR-AUD-006:** The system SHALL record verification results.
- **FR-AUD-007:** The system SHALL allow a completed decision to be replayed.
- **FR-AUD-008:** The normal application role SHALL NOT modify historical audit records.

## Traceability

The requirements above trace to `UN-001` through `UN-010` in
[`user-needs.md`](user-needs.md) and to `UC-001` through `UC-009` in
[`use-case-catalogue.md`](use-case-catalogue.md). Future implementation phases
must add concrete test IDs before marking requirements complete.
