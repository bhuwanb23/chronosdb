10. Phase 1H: Non-functional requirements
Goal

Define how well the system must operate.

10.1 Correctness
NFR-COR-001

For the frozen golden scenario, deterministic results must exactly match the approved expected outcomes.

## NFR-COR-002

Numerical fidelity must be 100% for displayed deterministic values.

## NFR-COR-003

All recommended interventions must pass feasibility validation.

## NFR-COR-004

The same scenario, state and rule version must produce the same output.

## 10.2 Performance

## Initial MVP targets:

| Operation | Target |
| --- | --- |
| Scenario validation | p95 below 200 ms |
| Baseline impact calculation | p95 below 2 seconds |
| One intervention simulation | p95 below 1 second |
| Five-candidate comparison | p95 below 5 seconds |
| Evidence retrieval | p95 below 2 seconds |
| Full response without LLM | p95 below 8 seconds |
| Full response with LLM | p95 below 15 seconds |
| Historical scenario replay | p95 below 3 seconds |


These are engineering targets to be tested later, not current performance claims.

10.3 Reliability
NFR-REL-001

A failed LLM call must not destroy deterministic simulation results.

## NFR-REL-002

A failed candidate simulation must not invalidate successful candidates.

## NFR-REL-003

The system must distinguish total failure from partial completion.

## NFR-REL-004

Scenario execution must be idempotent when the same idempotency key is used.

10.4 Security
All SQL must be parameterized.
Secrets must remain outside source control.
Database permissions must follow least privilege.
Audit records must not be mutable through the normal application role.
Prompt content must not override calculation authority.
Sensitive configuration must not appear in logs or API responses.
10.5 Explainability

## Every recommendation must expose:

Objective
Constraints
Candidate alternatives
Candidate metrics
Selection basis
Evidence references
Calculation version
Remaining risk
10.6 Usability

## The judge-facing workflow should:

Communicate the problem within 10 seconds.
Create a seeded scenario within three interactions.
Display the do-nothing impact without requiring chat.
Compare interventions on one screen.
Open evidence within one additional interaction.
Avoid requiring knowledge of SQL.
10.7 Accessibility

## Target:

Keyboard-accessible controls
Visible focus states
Non-color-only status indicators
Minimum WCAG AA contrast where practical
Labels for form controls
Text alternatives for charts
Responsive behavior at common laptop widths
10.8 Reproducibility

## A clean environment must be able to:

Configure Db2.
Run migrations.
Seed the dataset.
Start the application.
Execute the golden scenario.
Reproduce the documented result.

No undocumented data correction is permitted.

Deliverable
docs/product/non-functional-requirements.md

