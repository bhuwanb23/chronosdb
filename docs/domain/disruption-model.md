# Phase 2H: Event and Disruption Model

## MVP event

The first supported event type is `SUPPLIER_OUTAGE`.

Required parameters:

- `supplier_id`;
- `start_time`;
- exactly one of `end_time` or positive `duration`;
- `scope`;
- `severity`;
- `reported_time`.

Scope values are `ALL_SUPPLY`, `SELECTED_COMPONENTS`, or
`SELECTED_PURCHASE_ORDERS`. The golden scenario uses `ALL_SUPPLY`.

The event interval is `[start_time, end_time)`. An outage ending at its end
boundary no longer affects supply at that instant, subject to recovery lag.

## Affected supply rule

For an affected purchase order:

```text
outstanding = max(0, ordered_quantity - received_quantity)
new_arrival = max(original_arrival, outage_end + recovery_lag)
```

The first formula uses component quantity units; the second uses UTC
timestamps and a duration. Preconditions are non-negative quantities, a valid
outage interval, and a non-negative recovery lag. Invalid intervals or
missing arrival data produce `INSUFFICIENT_DATA`; no rounding is applied.

The initial configurable `recovery_lag` is two elapsed calendar days. The lag
represents supplier restart and logistics delay and must be recorded as an
assumption in each scenario.

Only outstanding quantity is delayed. Received quantity, cancelled orders,
unaffected suppliers, out-of-scope components, and orders arriving before the
outage are protected. An order after the outage remains unaffected when normal
capacity permits it.

## Post-outage simplification

Supply resumes at normal capacity after the recovery lag. Backlog-capacity
competition is not modeled in the MVP. This is an explicit assumption, not an
observed fact.

## Event precedence

The MVP supports one supplier outage per affected supply path. If overlapping
or multiple unmodeled disruptions affect the same supply, the scenario is
rejected with `UNSUPPORTED_OVERLAPPING_DISRUPTION`. The system must not guess
precedence or add effects twice. Multi-event precedence is deferred.

## Invariants

- Outage start precedes outage end.
- Recovery lag is non-negative and has an explicit time basis.
- Already received quantity is never delayed.
- An outage cannot affect an unrelated supplier or scope.
- A disruption cannot create or remove physical inventory directly; it changes
  expected receipt timing.
- Unsupported overlap is visible as a failure, not silently combined.
