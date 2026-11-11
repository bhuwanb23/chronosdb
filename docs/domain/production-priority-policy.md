# Phase 2K: Production Priority Policy

When capacity is constrained, order production by these keys in order:

1. in-progress status;
2. explicit production-order priority;
3. earliest associated customer promised delivery;
4. planned production start;
5. stable production-order ID.

The ordering is deterministic and applies identically to baseline and every
counterfactual candidate. A rescheduling intervention may change priority only
when it explicitly records the old and new priority and evaluates orders
helped and harmed.

## Capacity rules

- Facility daily capacity is expressed in finished-product units per day.
- Capacity already consumed by locked in-progress work is unavailable.
- A production order cannot reserve more capacity than its remaining quantity.
- A capacity calculation with missing facility data is
  `INSUFFICIENT_DATA`.
- Preemption of in-progress work is not allowed in the MVP.
