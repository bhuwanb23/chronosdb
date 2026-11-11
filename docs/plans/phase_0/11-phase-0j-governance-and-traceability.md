11. Phase 0J: Governance and Traceability
Goal

Prevent later design changes from becoming undocumented contradictions.

Required registers
docs/project-control/
├── project-charter.md
├── submission-status.md
├── requirements-register.csv
├── compliance-matrix.md
├── conflict-register.md
├── decision-log.md
├── assumption-register.md
├── risk-register.md
├── version-matrix.md
├── scope-register.md
└── phase-0-report.md

Decision log format
ADR-0001: Use LangChain as mandatory AI framework
Status: Accepted
Context:
Decision:
Alternatives:
Consequences:
Evidence:
Revisit condition:


### Initial architectural decision records:

ADR-0001 Use LangChain for typed planning and retrieval
ADR-0002 Use deterministic Python/SQL for all business calculations
ADR-0003 Use Db2 as system of record and evidence store
ADR-0004 Use FastAPI for backend APIs
ADR-0005 Lock supplier-outage as the first vertical slice
ADR-0006 Separate liveness from Db2 readiness
ADR-0007 Use synthetic data with explicit disclosure
ADR-0008 Never allow LLM-generated numerical business truth

## Risk scoring

### Use:

Risk Score=Likelihood(1−5)×Impact(1−5)\text{Risk Score} = \text{Likelihood}(1-5) \times \text{Impact}(1-5)

### Priority:

20–25: Critical
12–19: High
6–11: Medium
1–5: Low
Initial Phase 0 risks
| ID | Risk | Likelihood | Impact | Score | Treatment |
| --- | --- | --- | --- | --- | --- |
| R-001 | Submission deadline passed | 5 | 5 | 25 | Organizer confirmation |
| R-002 | Post-deadline commits rejected | 4 | 5 | 20 | Freeze or obtain permission |
| R-003 | Db2 vector feature unavailable | 3 | 5 | 15 | Verify version immediately |
| R-004 | Db2 setup unstable | 3 | 5 | 15 | Test restart and clean setup |
| R-005 | Secret committed | 2 | 5 | 10 | Gitleaks and protected config |
| R-006 | Scope expands beyond time | 4 | 4 | 16 | Lock MVP |
| R-007 | Repository validator fails | 2 | 5 | 10 | Run locally and in CI |
| R-008 | Framework-rule conflict | 3 | 4 | 12 | Include LangChain conservatively |
Acceptance criterion

### Every Critical and High risk must have:

Owner
Mitigation
Trigger
Contingency
Current status

No Critical Phase 0 risk may remain untreated.

