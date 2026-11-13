8. Phase 5D: Rule Registry and Version Control
Goal

Make every business calculation explicit and versioned.

Rule categories
Plain Text
STATE
SUPPLY
INVENTORY
BOM
ALLOCATION
PRODUCTION
FULFILMENT
SLA
FINANCIAL
CAUSAL
QUALITY
Rule identifier pattern
Plain Text
STATE-001
SUP-001
INV-001
BOM-001
ALLOC-001
PROD-001
FUL-001
SLA-001
FIN-001
CAU-001
DQ-001
xample rule definition
YAML
rule_id: INV-004
name: projected_inventory_balance
version: 1.0.0
description: >
Calculates projected component balance using opening inventory,
eligible receipts and ordered consumption events.
inputs:
- opening_available_quantity
- receipt_events
- consumption_events
- transfer_events
formula: >
prior_balance + receipts + transfers_in -
consumption - transfers_out
output:
- projected_balance
rounding: none
failure_condition:
- missing_opening_state
Rule-set manifest
JSON
{
"rule_set_version": "impact-rules-v1.0.0",
"domain_model_version": "2.0",
"dataset_compatibility": ["1.0.0"],
"rules": [
"STATE-001@1.0.0",
"SUP-001@1.0.0",
"INV-004@1.0.0"
]
}
Version rules
Patch

Implementation correction that does not alter intended business semantics.

Minor

Backward-compatible rule addition.

Major

Changed business semantics or changed benchmark outcomes.

A changed formula that alters frozen expected outputs requires:

New rule-set version
New benchmark review
Potential new dataset or expected-outcome version
Release notes
Deliverables
Plain Text
config/rules/impact-rules-v1.0.0.yaml
docs/impact-engine/rule-catalogue.md
Exit gate
Every computed field references a rule.
Every rule has typed inputs and outputs.
Rounding is defined.
Edge cases are defined.
Rule-set compatibility is recorded.
Hidden business logic in presentation code is prohibited.
