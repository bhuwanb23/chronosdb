# Determinism, Replay, and Idempotency

Execution identity is the SHA-256 hash of canonical scenario, state hash,
disruption, horizon, rule-set version, allocation policy, and scheduling
policy. Canonical output uses UTC timestamps, decimal strings, explicit nulls,
stable arrays, and stable rule versions.

Runtime-only values such as persistence timestamps are excluded from the
business result hash. Replaying the same fingerprint returns the immutable
stored result or verifies that a recalculation produces the same result hash.
