# 19O: Release Scorecard
Scores are not assigned where gate evidence is missing. Total is not computed because automatic-failure conditions are met.
| Category | Weight | Score | Basis |
|---|---|---|---|
| Business Value | 15 | 10 (provisional) | Golden revenue protection is real; untested with users |
| Innovation | 15 | not scored | Demo not rendered |
| Technical Quality | 15 | 5 (provisional) | 73 failed tests, 7 collection errors |
| Db2 Usage | 15 | not scored | Db2 not running in sandbox |
| Security | 10 | 6 (provisional) | 33/33 security tests pass; adversarial red; scanners not run |
| Reliability | 10 | 2 (provisional) | Replay test broken |
| Reproducibility | 10 | 0 | `make setup` fails |
| Documentation | 5 | 3 (provisional) | Claims needed removal |
| Demo Experience | 5 | 0 | No video |

**Decision band: Release Rejected (below 90, automatic failure).**
