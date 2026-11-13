31. Phase 5 Traceability Matrix

Create:

Plain Text
docs/impact-engine/phase-5-traceability-matrix.csv

Recommended columns:

Plain Text
phase1_requirement_id
phase2_rule_id
phase4_source_file
engine_module
function_or_service
rule_id
input_fields
output_fields
unit_test_ids
integration_test_ids
benchmark_scenario_ids
golden_evidence
status
notes

Example:

Plain Text
FR-IMP-012,
FIN-RAR-001,
demand/customer_order_lines.csv,
financial/revenue.py,
calculate_revenue_at_risk,
FIN-004,
late_quantity|unit_revenue,
revenue_at_risk,
UT-FIN-004,
IT-GOLD-001,
SCN-GOLD-001|SCN-0014,
golden/expected_do_nothing.json,
APPROVED,
Late quantity only
