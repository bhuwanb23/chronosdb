# Disruption Resolution

Supplier outage resolution matches supplier, scope, outstanding quantity,
eligible status, and expected-arrival timing. Outstanding quantity is
`max(0, ordered_quantity - received_quantity)`.

The disrupted arrival is:

```text
max(original_arrival, outage_end + recovery_lag)
```

Each impact preserves the original and changed timestamps, delay hours,
purchase-order/component/supplier identity, rule ID, and source record IDs.
