# Phase 2L: Customer Fulfilment Model

## Fulfilment assumptions

- Each customer-order line may link to one production order.
- One production order may fulfil multiple lines.
- Partial fulfilment is allowed.
- Completed product is allocated by customer priority and promised date.
- MVP shipping lead time is one elapsed calendar day.

## Projected delivery

```text
projected_delivery(line) =
    projected_product_availability(line)
  + delivery_lead_time
```

The promised date and projected delivery use an explicit time zone and
granularity.

## Partial fulfilment

```text
late_quantity(line) =
    max(0, ordered_quantity(line) - on_time_fulfilled_quantity(line))
```

Completed product allocated on time is not counted as late. Missing production
mapping or promised date returns `INSUFFICIENT_DATA`.

## Invariants

- A line cannot receive more product than ordered.
- Product cannot be allocated before projected availability.
- One completed product unit cannot fulfil two lines.
- Customer impact must retain the production and component causal references.
