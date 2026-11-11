# Phase 2P: Formula Catalogue

Every formula has an ID, inputs, units, output, preconditions, rounding rule,
edge behavior, owning requirement, and future implementation phase.

## Impact formulas

| ID | Formula | Output/unit | Preconditions and edge |
|---|---|---|---|
| IMP-001 | Component is affected when an expected receipt changes or a projected shortage exists relative to no-disruption baseline. | Boolean | Requires comparable baseline and disrupted projection; missing comparison is `INSUFFICIENT_DATA`. |
| IMP-002 | Production order is affected when projected start or completion changes because of disruption. | Boolean | Requires planned and projected UTC timestamps. |
| IMP-003 | Customer order is affected when any line's projected delivery changes. | Boolean | Requires line-to-production mapping and dates. |
| SLA-001 | `breached_order = exists line with late_quantity > 0`. | Boolean | Missing promised date is `INSUFFICIENT_DATA`; no rounding. |
| DEL-001 | `total_delay_hours = sum(late_quantity * delay_hours)` | Unit-hours | Quantity and delay units must be compatible; preserve decimal precision. |
| SLA-002 | `max_customer_delay = max(delay_hours)` | Hours | Empty set is zero only when no breach exists; missing delay is insufficient data. |
| SLA-003 | `average_breached_line_delay = sum(delay_hours) / breached_lines` | Hours | Denominator must be positive; no-breach result is not applicable. |

## Cost and value formulas

| ID | Formula | Output/unit | Preconditions and edge |
|---|---|---|---|
| COST-001 | `fixed_transfer_cost + quantity * variable_transfer_cost` | INR | Quantity and rates non-negative; no implicit currency conversion. |
| COST-002 | `fixed_expedite_fee + outstanding_quantity * expedite_unit_cost` | INR | PO outstanding and expedite feasible. |
| COST-003 | `quantity * max(0, alternate_unit_price - baseline_unit_price)` | INR premium | Cheaper alternate records savings separately; never negative intervention cost. |
| COST-004 | `reschedule_cost_per_order * affected_order_changes` | INR | Cost basis is configured and documented. |
| VALUE-001 | `max(0, revenue_at_risk_do_nothing - revenue_at_risk_candidate)` | INR | Both values use the same scenario, units, and reference case. |
| VALUE-002 | `revenue_protected - intervention_cost` | INR explanatory value | Not profit; revenue at risk is not confirmed loss. |

## Ranking formulas

| ID | Formula | Output/unit | Preconditions and edge |
|---|---|---|---|
| RANK-001 | `(x_i - min(x)) / (max(x) - min(x))` | Dimensionless [0,1] | If all values equal, normalized value is zero. |
| RANK-002 | `0.40*S_i + 0.30*R_i + 0.20*D_i + 0.10*C_i` | Dimensionless score | Weights sum to one; lower is better. |

## General rules

- Formula inputs must come from the scenario state, intervention overlay, or
  documented rule configuration.
- Quantity formulas preserve canonical component/product units.
- Money formulas use INR in the MVP and round only for presentation.
- Missing critical input is `INSUFFICIENT_DATA`, never zero.
- Formula versions are attached to derived results.
