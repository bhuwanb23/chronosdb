20. Phase 4P: Ground-Truth Outcome Generation
Goal

Calculate and freeze expected outcomes through the independent oracle.

Required oracle output

For every scenario:

JSON
{
"scenario_id": "SCN-XXXX",
"input_state_hash": "...",
"rule_version": "...",
"data_quality_status": "COMPLETE",
"do_nothing": {},
"candidates": [],
"optimal_set": [],
"recommended_intervention_id": "...",
"causal_traces": [],
"provenance": {}
}
Required intermediate outputs
Supply effect
Affected purchase orders
Changed receipt times
Changed quantities
Inventory effect
Opening balance
Receipts
Consumption
Transfers
Shortage timestamp
Shortage quantity
Production effect
Material-ready time
Capacity-ready time
Projected start
Projected completion
Delay
Customer effect
On-time quantity
Late quantity
Projected delivery
Delay
SLA status
Revenue at risk
Candidate effect
Feasibility
Rejection code
Cost
Outcome
Delta from do nothing
Ground-truth validation

For each expected recommendation:

Candidate is feasible.
Candidate satisfies budget.
Candidate satisfies approval constraints.
Candidate satisfies inventory constraints.
Candidate satisfies capacity constraints.
No better feasible candidate exists under the chosen objective.
Tie handling is correct.
Provenance is complete.
Oracle-versus-manual validation
Scenario class	Review requirement
Golden	Complete manual review
Demo supporting	Complete or high-detail review
Development	Automated validation
Validation	Automated plus sample manual review
Test	Automated plus stratified manual review
Adversarial	Explicit expected-error review
Deliverables
Plain Text
artifacts/phase-4/ground-truth/
├── expected-results.jsonl
├── intermediate-calculations.jsonl
├── causal-traces.jsonl
├── scenario-input-hashes.csv
└── ground-truth-review.md
