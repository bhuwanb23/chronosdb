28. Phase 3 Traceability Matrix

Create:

Plain Text
docs/data/phase-3-traceability-matrix.csv

Recommended columns:

Plain Text
phase2_rule_id
domain_entity
generated_file
generator_module
configuration_key
validation_rule
benchmark_scenario_ids
expected_output_field
ground_truth_function
phase4_target_table
status
notes

Example:

Plain Text
INV-TRANSFER-001,
Warehouse inventory,
inventory_snapshots.csv,
inventory.py,
safety_stock_ratio,
VAL-INV-008,
SCN-0012|SCN-0034,
expected_candidate_feasibility,
validate_transfer(),
INVENTORY_SNAPSHOT,
APPROVED,
Source safety stock enforced
