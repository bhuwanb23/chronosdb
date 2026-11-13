# Inventory Timeline

The inventory stage is a sparse event-driven calculation. It starts from the
latest as-of opening balance and applies only events at or before the
simulation horizon. Events are ordered by event time, documented precedence,
priority, and stable event identifier.

Physical balance is conserved as:

`ending = opening + receipts + transfers_in + returns + adjustments - issues - transfers_out - quarantine`

The result tracks physical balance, available balance, safety-stock threshold,
the first safety-stock breach, and the first material shortage separately.
Safety-stock exposure alone is not treated as a production shortage.

Operational records remain unchanged. Disrupted purchase orders become
projected receipt events in the impact result only.
