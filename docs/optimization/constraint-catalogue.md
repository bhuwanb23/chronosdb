# Phase 7D: Constraint Registry

The executable registry is `config/constraints/registry.yaml`, version
`phase7-constraints-v1`. It is parsed strictly; it is not prose or Markdown.

## Categories

| Category | Constraint | Rule | Severity |
|---|---|---|---|
| Cost | `max_recovery_cost` | ≤ ₹200,000 | HARD |
| Inventory | `min_remaining_inventory` | ≥ 0 above safety stock | HARD |
| Inventory | `max_inventory_commitment` | ≤ 500 units | HARD |
| Supplier | `supplier_approved` | must be active and approved when used | HARD |
| Supplier | `max_supplier_risk` | ≤ 0.35 | SOFT |
| Warehouse | `transfer_lane_approved` | lane must be active when used | HARD |
| Capacity | `max_capacity_utilization` | ≤ 100% | HARD |
| Delay | `max_delay_hours` | ≤ 240 hours (10 days) | HARD |
| Regulatory | `regulatory_compliance` | required when alternate supply is used | HARD |

## Semantics

- A HARD violation makes a candidate `INFEASIBLE`.
- A SOFT violation makes a candidate `CONDITIONALLY_FEASIBLE`.
- A constraint that does not apply to a plan (for example, supplier approval on
  a transfer-only plan) is recorded as `applicable: false` and does not fail the
  candidate. This prevents hidden assumptions.
- Overrides are explicit and produce a new in-memory constraint set. `max_cost`
  and `max_delay_days` are accepted API aliases; days are converted to hours.
- The live budget is ₹200,000. The live hybrid costs ₹852,400, so it is
  ineligible in the live scenario. The ₹132,000 hybrid expectation belongs to
  the frozen synthetic golden fixture.

Validator shape:

```yaml
version: "phase7-constraints-v1"
constraints:
  - constraint_id: CON-001
    name: max_recovery_cost
    category: COST
    operator: "<="
    value: 200000
    unit: INR
    severity: HARD
```
