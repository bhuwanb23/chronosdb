# Non-Functional Requirements

These are future validation targets for the product. They are not current
performance or accuracy claims.

## Correctness

- **NFR-COR-001:** For the frozen golden scenario, deterministic results must exactly match the approved expected outcomes.
- **NFR-COR-002:** Numerical fidelity must be 100% for displayed deterministic values.
- **NFR-COR-003:** All recommended interventions must pass feasibility validation.
- **NFR-COR-004:** The same scenario, state and rule version must produce the same output.

## Performance

Initial MVP targets:

- scenario validation: p95 under 200 ms;
- baseline impact calculation: p95 under 2 seconds;
- one intervention simulation: p95 under 1 second;
- five-candidate comparison: p95 under 5 seconds;
- evidence retrieval: p95 under 2 seconds;
- full response without LLM: p95 under 8 seconds;
- full response with LLM: p95 under 15 seconds;
- historical scenario replay: p95 under 3 seconds.

These are engineering targets to be tested later, not current performance claims.

## Reliability

- **NFR-REL-001:** A failed LLM call must not destroy deterministic simulation results.
- **NFR-REL-002:** A failed candidate simulation must not invalidate successful candidates.
- **NFR-REL-003:** The system must distinguish total failure from partial completion.
- **NFR-REL-004:** Scenario execution must be idempotent when the same idempotency key is used.

## Security

All SQL must be parameterized.
Secrets must remain outside source control.
Database permissions must follow least privilege.
Audit records must not be mutable through the normal application role.
Prompt content must not override calculation authority.
Sensitive configuration must not appear in logs or API responses.

## Explainability

Every recommendation must expose:

- Objective
- Constraints
- Candidate alternatives
- Candidate metrics
- Selection basis
- Evidence references
- Calculation version
- Remaining risk

## Usability

The judge-facing workflow should:

- Communicate the problem within 10 seconds.
- Create a seeded scenario within three interactions.
- Display the do-nothing impact without requiring chat.
- Compare interventions on one screen.
- Open evidence within one additional interaction.
- Avoid requiring knowledge of SQL.

## Accessibility

Target:

- Keyboard-accessible controls
- Visible focus states
- Non-color-only status indicators
- Minimum WCAG AA contrast where practical
- Labels for form controls
- Text alternatives for charts
- Responsive behavior at common laptop widths

## Reproducibility

A clean environment must be able to:

- Configure Db2.
- Run migrations.
- Seed the dataset.
- Start the application.
- Execute the golden scenario.
- Reproduce the documented result.

No undocumented data correction is permitted.

## Measurement rule

Every target must later record environment, sample size, median, p95, maximum,
and known limitations. Until measured, the target remains `PLANNED`.
