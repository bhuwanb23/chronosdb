6. Phase 14B: Reliability Strategy

Reliability is broader than correctness.

Reliability Pillars
Correctness
Produces correct output

Stability
Produces same output repeatedly

Recoverability
Recovers cleanly after failures

Transparency
Reports failures honestly

Isolation
Failures remain localized

Reliability Principle

Never hide failures.

Prefer:

PARTIALLY_COMPLETED


over:

COMPLETED


when uncertain.

Deliverable
docs/testing/reliability-strategy.md

