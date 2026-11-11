# Phase 2L: SLA and Revenue Model

## SLA classification

- `ON_TIME`: projected delivery is on or before the promised date.
- `BREACHED`: projected delivery is after the promised date.
- `AT_RISK`: optional warning when configured remaining margin is low.
- `INSUFFICIENT_DATA`: a required date or fulfilment relationship is missing.

The core benchmark uses only `ON_TIME` and `BREACHED`. The interface must
label whether it shows breached lines or breached customer orders.

## Delay

```text
customer_delay_hours(line) =
    max(0, projected_delivery(line) - promised_delivery(line))
```

The delay formula uses UTC timestamps and outputs hours. Missing promised or
projected delivery produces `INSUFFICIENT_DATA`; negative delay is clamped to
zero and is not rounded.

## Revenue at risk

```text
revenue_at_risk(line) =
    late_quantity(line) * unit_revenue(line)

total_revenue_at_risk =
    sum(revenue_at_risk(line))
```

Quantity and unit revenue must use compatible units and INR in the MVP. Money
retains fixed precision and is rounded to two decimal places only for
presentation. Missing quantity or revenue produces `INSUFFICIENT_DATA`.

This values only late or unfulfilled quantity. It is not confirmed revenue
loss.

## Breach counts

```text
breached_lines =
    count(lines where late_quantity > 0)

breached_orders =
    count(orders having at least one late line)
```

The recommended headline is projected customer orders breached.

## Invariants

- Partial late quantity produces partial revenue at risk.
- Missing due dates do not produce zero revenue at risk.
- A line and its parent order are separate metrics.
- Every financial result retains unit revenue, quantity, promised date,
  projected delivery, and causal evidence.
