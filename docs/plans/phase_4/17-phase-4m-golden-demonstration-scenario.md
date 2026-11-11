17. Phase 4M: Golden Demonstration Scenario
Goal

Freeze one visually compelling, completely verified demonstration.

Scenario
Plain Text
Scenario ID:
SCN-GOLD-001
 
As-of:
11 Nov 2026, 08:00 IST
 
Event:
SUP-0104 outage for 14 days
 
Objective:
MINIMIZE_SLA_BREACHES
 
Maximum recovery budget:
₹200,000
 
Simulation horizon:
30 days
Required candidate set
Do nothing
Transfer 400 MCU units
Alternate supplier for 400 MCU units
Expedition, feasible or explicitly rejected
Production rescheduling
Hybrid transfer plus alternate supplier
Infeasible 500-unit transfer
Required output classes

For each candidate:

Plain Text
feasibility_status
rejection_reason
intervention_cost
affected_production_orders
affected_customer_orders
sla_breach_count
revenue_at_risk
revenue_protected
total_delay
maximum_delay
evidence_references
causal_trace
Required golden headline result

Subject to the final independently verified timeline:

Plain Text
Do nothing:
2 breached customer orders
₹1,600,000 revenue at risk
 
Hybrid:
₹132,000 intervention cost
0 breached customer orders
₹0 revenue at risk
₹1,600,000 revenue protected
 
Expected recommendation:
Hybrid intervention
Timeline validation

The golden result cannot be frozen from rough dates alone. Produce an event timeline containing:

Inventory availability
Batch material issue
Batch production start
Batch completion
Product availability
Delivery readiness
Customer delivery
SLA comparison

Every event must have an exact timestamp.

Required independent checks
Reviewer A

Calculates the outcome from source records and formulas.

Reviewer B

Uses an independently prepared spreadsheet or calculation document.

Required agreement
Plain Text
100% for every headline and intermediate value
Golden artifacts
Plain Text
data/releases/v1.0.0/golden/
├── scenario.json
├── source_records/
├── state_at_as_of.json
├── disruption_overlay.json
├── candidate_interventions.json
├── expected_candidate_results.json
├── expected_recommendation.json
├── expected_timeline.json
├── expected_causal_traces.json
├── manual_calculation.csv
└── review_signoff.md
