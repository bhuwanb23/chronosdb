# Phase 2I: Inventory Availability Model

## Inventory position

For warehouse `w`, component `c`, and time `t`:

```text
available(w,c,t) =
    on_hand(w,c,t)
  - reserved(w,c,t)
  - quarantined(w,c,t)

usable(w,c,t) = max(0, available(w,c,t))
```

All inventory quantities use the component's canonical unit. Preconditions are
non-negative physical quantities, one warehouse/component/time position, and
non-overlapping authoritative snapshots. Missing or conflicting snapshots
produce `INSUFFICIENT_DATA`; no intermediate rounding is applied.

Physical on-hand is a fact. Available and usable inventory are derived values.
Safety stock is a planning threshold and is not automatically removed from
production availability.

## Projected balance

At ordered event times:

```text
balance(t) =
    balance(previous_t)
  + receipts(t)
  + transfers_in(t)
  - production_consumption(t)
  - transfers_out(t)
```

Balance inputs and output use the component unit and event time. A receipt,
transfer, or consumption event without a valid timestamp is invalid. Negative
physical on-hand is a data-quality failure, not a value to clamp silently.

Receipts cannot be consumed before their arrival time. A counterfactual balance
is derived from the baseline and overlays; it does not mutate physical
on-hand.

## Safety-stock behavior

Production may consume below safety stock when required, and the breach is
recorded as operational risk. An optional warehouse transfer may not reduce
the source warehouse below protected safety stock.

## Shortage

A shortage exists when a material requirement cannot be fully allocated by its
required consumption time:

```text
shortage_quantity = max(0, required_quantity - allocatable_quantity)
```

The shortage formula requires matching component units and a requirement time.
The result is rounded only when the component unit requires whole units, using
the BOM requirement rule.

The shortage date is the earliest requirement time where projected balance is
less than the requirement at that time.

## Transfer availability

For a source warehouse:

```text
transferable_quantity =
    max(0, projected_balance_before_transfer
           - safety_stock
           - committed_future_demand)
```

Transfer quantity uses the component unit and requires a scenario horizon,
source safety stock, and committed future demand. Missing protection-window
inputs produce `INSUFFICIENT_DATA`.

The protected-demand window is the scenario horizon unless a narrower,
documented transfer-protection window is explicitly selected.

## Invariants

- Physical on-hand cannot become negative.
- Allocated quantity cannot exceed eligible available quantity.
- Transfer quantity cannot exceed transferable quantity.
- One inventory quantity cannot be allocated to two production orders.
- Existing reservations are not subtracted twice.
- A receipt is unavailable before its arrival.
