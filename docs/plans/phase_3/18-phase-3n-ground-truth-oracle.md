18. Phase 3N: Ground-Truth Oracle
Goal

Generate expected outcomes independently from future application services.

The ground-truth oracle is the most important part of Phase 3.

Independence requirement

The Phase 5 production impact engine must not simply import its expected outputs from the oracle.

Recommended separation:

Plain Text
src/ground_truth/
src/application/

The oracle should prioritize clarity and correctness over speed.

Oracle responsibilities
Reconstruct state at the scenario as-of time.
Apply the disruption.
Calculate outstanding receipt changes.
Build inventory timelines.
Allocate components.
Schedule production.
Allocate finished products to customer lines.
Calculate delivery and SLA status.
Calculate revenue at risk.
Apply candidate overlays.
Validate feasibility.
Calculate candidate outcomes.
Rank feasible candidates.
Emit causal traces.
Emit expected outcomes.
Oracle design

Use small, explicit functions:

Plain Text
select_active_records()
calculate_outstanding_quantity()
apply_supplier_outage()
build_inventory_timeline()
allocate_material()
schedule_production()
allocate_customer_fulfilment()
calculate_sla()
calculate_revenue_at_risk()
validate_intervention()
apply_intervention()
rank_candidates()
build_causal_trace()
Explainability requirement

The oracle must emit intermediate calculations, not only final metrics.

Example:

JSON
{
"component_id": "CMP-MCU-42",
"warehouse_id": "WH-PUNE",
"opening_balance": 400,
"receipts": [],
"consumption": [
{
"production_order_id": "MO-0876",
"quantity": 400,
"time": "2026-11-12T00:00:00Z"
}
],
"first_shortage_time": "2026-11-15T00:00:00Z",
"shortage_quantity": 400
}
Numerical determinism
Use decimal arithmetic for money.
Avoid binary floating point for financial values.
Define timestamp boundaries.
Use stable sort keys.
Use explicit rounding.
Hash input state and outputs.
Ground-truth review

For all scenarios:

Automated invariant validation

For golden scenarios:

Full manual validation

For test scenarios:

At least sample-based independent review
Deliverables
Plain Text
src/ground_truth/
tests/ground_truth/
artifacts/ground_truth/
