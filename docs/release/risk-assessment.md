# 19N: Risk Assessment
| Category | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| Technical | Replay broken in live demo | High (test already fails) | High | Fix D-01; pre-recorded backup |
| Technical | Setup fails for judges | High | High | Fix D-02; provide Docker or frozen-output path |
| Security | Adversarial suite red | Medium | High | Fix tests; run live red-team |
| Product | Judge sees claims that cannot be reproduced | High | High | Remove unverified claims; re-measure |
| Submission | Missing PR/form/identity | High | High | User supplies details |
| Demo | Video missing or late | High | High | Render on GPU now; backup screenshots |
| Submission | Repo push deletes data | Medium | High | User handles repo; do not push deleted state |
