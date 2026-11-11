16. Final Phase 0 Gate Checklist
Submission safety
 Registration status documented
 Existing PR status documented
 Google Form status documented
 LinkedIn requirement documented
 Deadline conflict resolved
 Post-deadline update permission resolved
 Participation mode resolved
 Framework requirement resolved
Repository
 Canonical repository used
 submission/chronosdb branch exists
 submissions/chronosdb directory exists
 Required four files exist
 submission.json is valid
 Official validator passes three times
 No unrelated files changed
Environment
 Versions are recorded
 Dependencies are locked
 Clean installation succeeds
 Make targets work
 No undocumented global dependency exists
Db2
 Actual Db2 instance is available
 Exact version is recorded
 Application connects successfully
 Health table write/read works
 Restart recovery works
 Vector capability is explicitly verified
 Baseline performance is recorded
Application
 Liveness endpoint works
 Readiness endpoint works
 Db2 failure is detected
 Configuration failure is clear
 No credential appears in responses or logs
Quality
 Linter passes
 Type checker passes
 Foundation tests pass
 CI passes three times
 No flaky foundation test remains
Security
 .env is ignored
 .env.example contains dummy values
 Working tree has no secrets
 Git history has no secrets
 No critical vulnerability is ignored
 Dependency licenses are inventoried
Governance
 Product charter complete
 Requirements register complete
 Conflict register complete
 Decision log complete
 Risk register complete
 Assumption register complete
 Phase 0 report complete
Handoff
 Foundation benchmark score is at least 90
 No automatic-failure condition exists
 Foundation commit is recorded
 Foundation tag is created when allowed
 Phase 1 inputs are complete
