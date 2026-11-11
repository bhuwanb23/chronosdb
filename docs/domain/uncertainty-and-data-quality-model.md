# Phase 2R: Uncertainty and Data-Quality Model

## Information classes

- `OBSERVED`: directly stored operational fact.
- `DERIVED`: deterministic result from observed facts and rules.
- `ASSUMED`: configured simplification, such as one-day delivery or two-day
  recovery lag.
- `PROJECTED`: future outcome from deterministic scenario evaluation.
- `GENERATED`: AI-produced explanation constrained by verified results.

Generated text never overrides observed or derived values.

## Completeness states

- `COMPLETE`: all critical inputs are present and valid.
- `PARTIAL_NONCRITICAL`: noncritical information is missing.
- `PARTIAL_CRITICAL`: a critical calculation input is missing.
- `INVALID`: data violates a domain invariant.

Critical missing examples include no active BOM, no inventory state, missing
promised delivery, missing production mapping, or unknown supplier relation.
The affected calculation must block with `INSUFFICIENT_DATA`.

## Missing versus zero

Missing values are never converted to zero. Use distinct states:

- `UNKNOWN`: expected information is unavailable;
- `NOT_APPLICABLE`: field does not apply;
- `ZERO`: explicitly observed or derived zero.

This applies to inventory, cost, lead time, revenue, and demand.

## Evidence classification

- `HIGH_EVIDENCE`: critical records complete, no major assumption drives the
  result, and causal trace is complete.
- `MEDIUM_EVIDENCE`: critical records complete but configured assumptions affect
  timing or cost.
- `LOW_EVIDENCE`: noncritical data is missing or result is assumption-sensitive.
- `INSUFFICIENT_EVIDENCE`: a critical calculation cannot be completed.

No arbitrary percentage confidence is generated.

## Partial-result policy

Safe unaffected results remain visible when a separate affected calculation is
blocked. The blocked result names its missing input and status. Invalid data
must be corrected or replaced by a new state version; it is not silently
repaired.
