# Deterministic Impact Engine Contract

The calculation boundary is a pure function:

```text
calculate_impact(operational_state, disruption, horizon, rule_set) -> ImpactResult
```

It may depend only on the reconstructed state identity, disruption definition,
simulation horizon, rule-set version, allocation policy, scheduling policy, and
calendar configuration. It does not read expected benchmark outcomes.

All records are explicitly sorted by stable identifiers, timestamps are UTC,
quantities use decimal serialization, and results are canonicalized before
hashing. SQL, HTTP, wall-clock time, network calls, LLM output, mutable global
state, and unseeded randomness are outside the calculation layer.
