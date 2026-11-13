20. Phase 5P: Idempotency, Replay, and Determinism
Goal

Guarantee stable and reproducible results.

Execution identity

Construct a deterministic execution key from:

Plain Text
scenario ID
state hash
disruption hash
simulation horizon
rule-set version
allocation policy
scheduling policy
Request fingerprint
Fingerprint=SHA256(CanonicalRequest+StateHash+RuleSetVersion)Fingerprint = SHA256( CanonicalRequest + StateHash + RuleSetVersion )Fingerprint=SHA256(CanonicalRequest+StateHash+RuleSetVersion)
Idempotency behavior

When the same fingerprint is submitted:

Return the existing completed result, or
Recalculate and confirm the same result hash in explicit verification mode

Do not create conflicting duplicate results.

Result hash

Canonicalize:

All deterministic output fields
Stable array ordering
UTC timestamps
Decimal strings
Explicit nulls
Rule versions

Exclude:

Execution duration
Runtime host ID
Log correlation ID
Creation timestamp, if it is not business-semantic
Determinism benchmark

Run the golden scenario:

Plain Text
100 times

Target:

Plain Text
Unique business result hashes: 1
Value mismatches: 0
Ordering mismatches: 0

Run a representative set of 20 benchmark scenarios:

Plain Text
10 times each

Target:

Plain Text
200/200 stable result hashes
Cross-process test

Run the same scenario:

In separate processes
After service restart
With different thread scheduling
After database restart

Expected business result remains identical.

Deliverables
Plain Text
docs/impact-engine/determinism-contract.md
artifacts/phase-5/determinism-report.json
