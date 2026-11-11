17. Phase 3M: Benchmark Scenario Suite
Goal

Build a frozen evaluation set broad enough to measure correctness without diluting the core supplier-outage focus.

Recommended 60-scenario suite
Scenario category	Count
Full supplier outage	18
Partial supplier outage	8
Selected-component outage	6
Purchase-order-specific disruption	4
Inventory-transfer constraint	4
Alternate-supplier constraint	4
Budget-constrained recovery	4
No operational impact	3
No feasible intervention	3
Insufficient critical data	3
Tie or Pareto-equivalent outcome	3
Total	60
Difficulty split
Plain Text
Level 1: 15 scenarios
Level 2: 20 scenarios
Level 3: 17 scenarios
Level 4: 8 scenarios
Outcome labels

Each scenario must include:

Plain Text
expected_validity
expected_affected_components
expected_shortages
expected_affected_production_orders
expected_affected_customer_orders
expected_sla_breaches
expected_revenue_at_risk
expected_candidate_feasibility
expected_candidate_metrics
expected_optimal_set
expected_recommendation
expected_data_quality_state
expected_causal_trace_roots
Multiple valid recommendations

Do not force a single expected recommendation when:

Candidates tie
Multiple candidates are Pareto-efficient
Objective weights create equivalent scores

Use:

JSON
{
"expected_optimal_set": [
"INT-SCN-0042-B",
"INT-SCN-0042-D"
],
"tie": true
}
Dataset partitions

Recommended:

Partition	Scenarios
Development	24
Validation	12
Test	18
Golden	3
Adversarial-only	3

The golden scenarios may also be referenced separately from the 60 broad scenarios, but duplication must be explicit.

Deliverables
Plain Text
data/benchmarks/
├── scenarios/
├── expected/
├── partitions.json
├── benchmark_manifest.json
└── scenario_catalogue.csv
