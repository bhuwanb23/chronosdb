# Non-Functional Requirements

These are future validation targets for the product. They are not current
performance or accuracy claims.

## Correctness

- **NFR-COR-001:** The frozen golden scenario SHALL match its approved
  deterministic outcomes exactly.
- **NFR-COR-002:** Displayed deterministic numbers SHALL match structured
  outputs 100% of the time.
- **NFR-COR-003:** Every recommended intervention SHALL pass feasibility
  validation.
- **NFR-COR-004:** Identical state, input, and rule version SHALL be
  reproducible.

## Performance targets

Measured locally after the domain workflow exists:

- scenario validation: p95 under 200 ms;
- baseline impact: p95 under 2 seconds;
- one intervention simulation: p95 under 1 second;
- five-candidate comparison: p95 under 5 seconds;
- evidence retrieval: p95 under 2 seconds;
- full deterministic response: p95 under 8 seconds.

## Reliability

- A failed optional AI call SHALL preserve deterministic results.
- A failed candidate SHALL not invalidate successful candidates.
- The system SHALL distinguish total failure, partial completion, and
  insufficient data.
- Repeating a request with the same idempotency key SHALL not create
  inconsistent duplicate execution.

## Security and privacy

- All SQL SHALL be parameterized.
- Secrets SHALL remain outside source control, logs, and API responses.
- Db2 permissions SHALL follow least privilege.
- Normal application access SHALL not mutate audit history.
- External text SHALL not override calculation authority or access filters.

## Explainability

Every recommendation SHALL expose its objective, constraints, candidates,
metrics, selection basis, evidence references, rule version, and remaining
risk.

## Usability and accessibility

- The primary problem should be understandable within 10 seconds.
- A seeded scenario should be startable within three user interactions.
- Baseline and comparison results should be visible without using chat.
- Controls should support keyboard use, visible focus, labels, and
  non-color-only status indicators.
- Charts and status visuals must have text alternatives.

## Reproducibility

A clean environment must be able to configure Db2, apply migrations, seed the
future dataset, run the golden scenario, and reproduce the documented result
without undocumented manual data correction.

## Measurement rule

Every target must later record environment, sample size, median, p95, maximum,
and known limitations. Until measured, the target remains `PLANNED`.
