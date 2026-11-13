7. Phase 5C: Input and Output Model
Goal

Define precise typed contracts for engine execution.

7.1 Impact request
JSON
{
"scenario_id": "SCN-GOLD-001",
"as_of_time": "2026-11-11T02:30:00Z",
"simulation_end_time": "2026-12-11T02:30:00Z",
"disruption_event_id": "EVT-GOLD-001",
"rule_set_version": "impact-rules-v1.0.0",
"allocation_policy": "priority-due-date-v1",
"scheduling_policy": "batch-capacity-v1"
}
7.2 Input-state identity
JSON
{
"dataset_version": "1.0.0",
"state_version": "STATE-GOLD-001",
"state_hash": "sha256-value",
"as_of_time": "2026-11-11T02:30:00Z"
}
7.3 Top-level impact result
JSON
{
"impact_run_id": "IR-...",
"scenario_id": "SCN-GOLD-001",
"status": "COMPLETED",
"data_quality_status": "COMPLETE",
"rule_set_version": "impact-rules-v1.0.0",
"input_state_hash": "...",
"result_hash": "...",
"affected_purchase_orders": [],
"affected_components": [],
"inventory_timelines": [],
"shortages": [],
"affected_production_orders": [],
"affected_customer_orders": [],
"headline_metrics": {},
"causal_traces": [],
"warnings": [],
"errors": [],
"provenance": {}
}
7.4 Headline metrics
JSON
{
"affected_supplier_count": 1,
"affected_purchase_order_count": 1,
"supply_affected_component_count": 1,
"shortage_affected_component_count": 1,
"affected_production_order_count": 2,
"affected_customer_order_count": 2,
"sla_breached_customer_order_count": 2,
"late_quantity": 400,
"total_delay_unit_hours": 110400,
"maximum_delay_hours": 288,
"revenue_at_risk": {
"amount": "1600000.00",
"currency": "INR"
}
}

The exact delay values must come from the frozen golden timeline.

7.5 Status values
Plain Text
PENDING
VALIDATING
RECONSTRUCTING_STATE
APPLYING_DISRUPTION
PROJECTING_INVENTORY
SCHEDULING_PRODUCTION
CALCULATING_CUSTOMER_IMPACT
BUILDING_PROVENANCE
COMPLETED
PARTIALLY_COMPLETED
REJECTED
FAILED
Deliverables
Plain Text
docs/impact-engine/input-contract.md
docs/impact-engine/output-contract.md
schemas/impact-request.schema.json
schemas/impact-result.schema.json
