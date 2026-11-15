# 19M: Final Defect Register
| ID | Severity | Finding | Evidence |
|---|---|---|---|
| D-01 | **S1** | Golden determinism / replay test broken (`execute_scenario` undefined) | pytest tests/reliability |
| D-02 | **S1** | Setup broken (`make setup` needs missing `docker/frontend`) | Makefile, repo listing |
| D-03 | **S1** | Demo video missing | assets/demo |
| D-04 | **S1** | Submission artifacts missing (PR, form, participant identity) | docs/submission |
| D-05 | **S1** | Test suite: 73 failed, 4 collection errors | pytest run |
| D-06 | **S1** | `chronosdb.config.Settings` missing; Db2 integration test cannot import | pytest collect |
| D-07 | **S1** | Undefined names in unit/schema tests (`validate_schema`, `verify_numbers`, `schedule_production`, `project_inventory`, `process_supplier`) | pytest NameError |
| D-08 | S2 | 56 test failures depend on data removed in the size cleanup (`data/releases`, `EVT-GOLD-*`) | pytest |
| D-09 | S2 | Retrieval metrics (Recall@5, MRR) not re-measured; previously shown figures were not engine output | docs/demo/verified-golden-figures.md |
| D-10 | S2 | Public GitHub repo lacks LICENSE and Phase 16/17 files | GitHub API |
| D-11 | S2 | Local git: 945 deleted tracked files; pushing would delete data from GitHub | git status |
| D-12 | S2 | Evidence Explorer and architecture diagram show empty boxes for emoji icons | screenshots |
| D-13 | S3 | `src/frontend/playwright-report/` generated report in repo | repo listing |
| D-14 | S2 | Earlier phase reports claimed passing results that do not reproduce now (e.g., Phase 14 "Golden Pass 100%") | pytest vs audit reports |

Severity-1 open: **7**. Gate rule: no open S1. **Fails.**
