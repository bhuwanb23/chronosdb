# Product Risk Register

| ID | Risk | Impact | Treatment | Trigger |
|---|---|---|---|---|
| P1-R01 | Scope expands beyond the supplier-outage slice. | Critical | Enforce P0–P3 register and change rule. | New feature lacks priority or acceptance test. |
| P1-R02 | Revenue-at-risk is interpreted as confirmed loss. | High | Freeze the definition and show units/rule. | Narrative uses “revenue lost” without proof. |
| P1-R03 | AI receives calculation authority. | Critical | Enforce the AI authority contract and claim verifier. | AI output changes a metric or feasibility state. |
| P1-R04 | Simulation is presented as real-world prediction. | High | Use “counterfactual projection” terminology. | Documentation claims certainty or prediction. |
| P1-R05 | Requirements cannot be tested. | High | Require IDs, traceability, and acceptance coverage. | Requirement has no verification path. |
| P1-R06 | Db2 is only decorative storage. | High | Store operational state, scenario, evidence, and audit data in Db2. | A feature can work without its Db2 evidence path. |
| P1-R07 | Synthetic data appears unrealistic. | High | Define domain rules and manually verify a golden scenario. | Seed data violates a domain constraint. |
| P1-R08 | Optimization recommends an infeasible action. | Critical | Apply hard feasibility gates before ranking. | Recommended candidate has a hard-constraint violation. |
| P1-R09 | No feasible plan is hidden. | High | Return explicit `NO_FEASIBLE_INTERVENTION`. | All candidates fail but one is still selected. |
| P1-R10 | Metrics are selected after results are observed. | High | Freeze the measurement contract before implementation. | A result uses an undocumented metric or denominator. |
| P1-R11 | Missing data is treated as zero. | Critical | Return `INSUFFICIENT_DATA` with the missing field. | A calculation completes using an absent fact. |

Critical risks require a failing test or explicit review evidence before the
dependent phase can pass.
