# Phase 7F: Metric Definitions

All metrics are extracted from Phase 6 `CounterfactualResult` and the frozen
Phase 5 operational state. No metric is estimated by an LLM.

| Metric | Definition | Direction |
|---|---|---|
| `revenue_risk` | Phase 6 scenario revenue at risk | lower is better |
| `revenue_protected` | baseline revenue at risk minus scenario revenue at risk | higher is better |
| `sla_breaches` | scenario breached customer-order count | lower is better |
| `breaches_avoided` | baseline breaches minus scenario breaches | higher is better |
| `delay_hours` | scenario maximum customer delay | lower is better |
| `delay_reduction_hours` | baseline maximum delay minus scenario maximum delay | higher is better |
| `recovery_cost` | Phase 6 intervention cost | lower is better |
| `capacity_utilization_pct` | supplied quantity divided by active supplier capacity over the lead time | lower is better |
| `inventory_consumed` | transfer units plus alternate-supplier units committed by the plan | lower is better |
| `remaining_inventory` | lowest post-plan buffer above safety stock across touched component warehouses | higher is better |
| `supplier_risk` | operational-risk-v1 policy: action base + capacity pressure + lead-time pressure | lower is better |

## Inventory Notes

- A transfer moves stock between warehouses; it does not add stock. The source
  warehouse buffer is therefore included in `remaining_inventory`.
- An alternate supplier and an expedition add receipts.
- Expedition receipts are procurement, not inventory commitment, so they do not
  consume the `max_inventory_commitment` allowance.
- `remaining_inventory` is clamped at zero above safety stock. A source-stock
  violation cannot be hidden by another warehouse's surplus.

## Risk Policy

`operational-risk-v1` is deliberately simple and versioned:

- Transfer base: 0.05
- Reschedule base: 0.10
- Alternate supplier base: 0.15, plus lead-time pressure above 3 days
- Expedition base: 0.25
- Multiple actions: +0.05
- Capacity pressure: +0.10 × utilization (capped at 100%)
- Final score capped to `[0, 1]`

This is an explicit policy, not a learned or hidden supplier score.
