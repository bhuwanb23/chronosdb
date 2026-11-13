# Phase 5 Golden Comparison

- Scenario: `SCN-GOLD-001`
- State hash: `47e178713708fe62e1eee1c68edbaa448fb88a519c418221a6fa31f96142b286`
- Rule set: `impact-rules-v1.0.0`
- Result hash: `1459e495b540dce3e5bc971ad38da0b983e391effcc11f011f3bab95559d0d18`

All frozen checks passed:

- `breached_customer_order_count`: `2`
- `late_quantity`: `400`
- `total_delay_unit_hours`: `110400`
- `revenue_at_risk`: `1600000.00`
- `affected_purchase_orders`: `['PO-2208']`
- `affected_components`: `['CMP-MCU-42']`
- `affected_production_orders`: `['MO-0882', 'MO-0889']`
- `affected_customer_orders`: `['CO-0704', 'CO-0711']`
- `customer_line_fidelity`: `True`
- `causal_path_fidelity`: `True`
- `causal_trace_exact`: `True`
- `causal_trace_count`: `2`
