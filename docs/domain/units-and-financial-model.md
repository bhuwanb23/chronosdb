# Phase 2F: Units, Quantities, and Financial Model

## Unit policy

Every quantity carries a unit. The golden electronic-components scenario uses
`EA` (each) for component and finished-product quantities. `KG`, `L`, and `M`
are recognized conceptual examples but are not mixed with `EA`.

Incompatible units are rejected. Conversion is out of the MVP unless an
explicit conversion rule is defined.

## Precision

- Component quantities use decimal precision conceptually.
- Discrete finished-product quantities are integer quantities.
- Money uses fixed decimal precision.
- Percentages are decimals from 0 through 1.
- Internal values retain full precision.
- Presentation rounds INR to two decimal places.
- Intermediate quantities are not rounded unless the unit requires whole
  units; then they are rounded upward at the requirement boundary.

## Currency

The MVP uses INR for all golden-scenario costs and revenue. Multi-currency
conversion is deferred. Money with different currencies cannot be added,
compared, or ranked without an explicit conversion rule.

## Inventory quantities

```text
available = on_hand - reserved - quarantined
usable = max(0, available)
```

Safety stock is a planning threshold, not automatically unavailable material.
Production may consume below it when required, but an optional transfer may not
reduce the source warehouse below its protected threshold. Any resulting
safety-stock breach is recorded as risk.

## Revenue

For an order line:

```text
line_revenue = ordered_quantity * unit_revenue
revenue_at_risk = late_or_unfulfilled_quantity * unit_revenue
```

Revenue at risk is not confirmed revenue loss and does not automatically equal
the full order-line revenue when only part of the quantity is late.

## Intervention cost

```text
intervention_cost =
    purchase_price_premium
  + expedite_fee
  + transfer_cost
  + rescheduling_penalty
  + modeled_overtime_cost
```

Only modeled and applicable components are included. A cost must not be counted
both in a candidate parameter and again in a derived total.

## Financial invariants

- Every amount has a currency.
- Every cost component has a clear owner and inclusion rule.
- Revenue-at-risk values have quantity and unit-revenue evidence.
- Negative quantities, costs, and revenues are invalid unless a later domain
  rule explicitly models a reversal.
- Rounding occurs at presentation or defined discrete-quantity boundaries, not
  silently inside formulas.
