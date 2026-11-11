# ChronosDB Product Contract

This folder contains the documentation-only contract for Phase 1A–1Q. It
defines what ChronosDB is, who it serves, which decision it supports, how a
user moves through it, what later implementation must satisfy, and how Phase 2
must be evaluated.

## Work packages

### Product contract — Phase 1A–1D

- [`phase-0-handoff-review.md`](phase-0-handoff-review.md)
- [`product-identity.md`](product-identity.md)
- [`stakeholder-map.md`](stakeholder-map.md)
- [`primary-persona.md`](primary-persona.md)
- [`user-needs.md`](user-needs.md)
- [`decision-specification.md`](decision-specification.md)

### Workflow contract — Phase 1E–1F

- [`end-to-end-user-journey.md`](end-to-end-user-journey.md)
- [`use-case-catalogue.md`](use-case-catalogue.md)

### Requirement and data contract — Phase 1G–1I

- [`functional-requirements.md`](functional-requirements.md)
- [`non-functional-requirements.md`](non-functional-requirements.md)
- [`data-and-evidence-requirements.md`](data-and-evidence-requirements.md)

### Control and evaluation contract — Phase 1J–1M

- [`ai-authority-contract.md`](ai-authority-contract.md)
- [`scope-and-priority-register.md`](scope-and-priority-register.md)
- [`rubric-evidence-matrix.csv`](rubric-evidence-matrix.csv)
- [`measurement-contract.md`](measurement-contract.md)

The evidence matrix is an internal product-proof map. It is not a competition
or submission rubric.

### Acceptance, risk, and handoff — Phase 1N–1Q

- [`product-acceptance-tests.md`](product-acceptance-tests.md)
- [`product-risk-register.md`](product-risk-register.md)
- [`product-assumption-register.md`](product-assumption-register.md)
- [`phase-2-question-register.md`](phase-2-question-register.md)
- [`requirements-traceability-matrix.csv`](requirements-traceability-matrix.csv)
- [`phase-1-completion-report.md`](phase-1-completion-report.md)

## Locked assumptions

- Primary user: supply-chain operations manager.
- First scenario: critical supplier outage.
- Db2 is the operational and evidence system of record.
- Deterministic code owns numerical business outcomes.
- Recommendations require human review.
- The MVP is a single supplier-outage vertical slice.
- Phase 1J–1Q is documentation-complete; implementation remains deferred.

## Phase 2 handoff

Phase 2 should translate this contract into the domain model, causal
relationships, time semantics, units, and business rules. It should not infer
new product scope from implementation convenience.
