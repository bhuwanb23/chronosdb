12. Phase 0K: Foundation Benchmarking
Goal

Prove that the project foundation is stable enough for Phase 1.

This is not the product benchmark. It measures setup, compliance, connectivity and engineering health.

Benchmark suite
B0-01 Submission validation
Input: submissions/chronosdb
Runs: 3
Target: 3/3 passes

### B0-02 Clean-install reproducibility

Perform from a clean checkout.

### Measure:

Installation success
Time to ready
Manual interventions
Missing instructions
Package conflicts

### Target:

Success: 100%
Undocumented manual steps: 0
Package conflicts: 0

B0-03 Db2 connectivity reliability
Warm-up: 5 calls
Measured calls: 50
Target success rate: 100%
Target p95: <500 ms locally

B0-04 Restart recovery
Stop Db2.
Confirm readiness fails.
Restart Db2.
Confirm readiness recovers.
Run read/write verification.

### Target:

Correct failure detection: 100%
Correct recovery detection: 100%
Data loss: 0
Manual code changes: 0

### B0-05 Secret scan

### Run against:

Working tree
Git history
Config files
Documentation
Screenshot folder

### Target:

## Verified secrets: 0

### B0-06 CI repeatability

Run the full foundation pipeline three times.

### Target:

Passes: 3/3
Flaky tests: 0
Result differences: 0

### B0-07 Error-quality test

### Trigger:

Missing DB2_HOST
Invalid credentials
Db2 unavailable
Invalid port

### Target:

Clear actionable internal logs
Sanitized user response
No password exposure
Correct non-zero command exit or non-ready status
Phase 0 Foundation Score

Use a strict gate, not a vanity score.

| Category | Weight | Passing condition |
| --- | --- | --- |
| Submission certainty | 25 | Eligibility and update permission documented |
| Compliance | 15 | 100% mandatory requirement coverage |
| Repository validity | 10 | Validator passes 3/3 |
| Environment reproducibility | 15 | Clean install succeeds |
| Db2 reliability | 15 | Connectivity and restart tests pass |
| CI and quality | 10 | Pipeline passes 3/3 |
| Security and licensing | 10 | No secrets or critical vulnerabilities |
| Total | 100 |  |
Required result
90–100: Phase 0 passes
80–89: Conditional pass; no critical defect permitted
Below 80: Phase 0 fails


### However, the following are automatic failures regardless of score:

Eligibility remains unknown.
A real secret exists in Git history.
Official validator fails.
Application cannot connect to actual Db2.
Required submission files are missing.
Clean checkout cannot run.
Critical dependency vulnerability is ignored.
Organizer explicitly rejects continued participation.
