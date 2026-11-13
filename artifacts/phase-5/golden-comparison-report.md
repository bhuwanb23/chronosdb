# Phase 5 Golden Comparison

- Scenario: `SCN-GOLD-001`
- State hash: `47e178713708fe62e1eee1c68edbaa448fb88a519c418221a6fa31f96142b286`
- Rule set: `impact-rules-v1.0.0`
- Result hash: `3f63cf014ec38ec48898b06eacf9fa9fc18dc3f61595d4d10ccaf84218021eeb`

All frozen checks passed:

- `breached_customer_order_count`: `2`
- `late_quantity`: `400`
- `total_delay_unit_hours`: `110400`
- `revenue_at_risk`: `1600000.00`
- `affected_purchase_orders`: `['PO-2208']`
- `affected_components`: `['CMP-MCU-42']`
- `affected_production_orders`: `['MO-0882', 'MO-0889']`
- `affected_customer_orders`: `['CO-0704', 'CO-0711']`
- `causal_trace_count`: `2`
