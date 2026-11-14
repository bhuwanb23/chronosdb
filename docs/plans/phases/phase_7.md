Phase 7 Deep Dive: Intervention Optimization Engine
Select the Best Feasible Recovery Plan Under Explicit Business Constraints

Phase 6 answered:

"What happens if we apply intervention X?"

Phase 7 answers:

"Which intervention should we choose, and why?"

This is where ChronosDB evolves from a simulation system into a true decision-support platform.

Phase 5 produced:

Do-Nothing Impact


Phase 6 produced:

Transfer Result
Expedite Result
Alternate Supplier Result
Production Reschedule Result
Hybrid Result


Phase 7 must:

Validate feasibility
Compare outcomes
Evaluate trade-offs
Identify Pareto-efficient plans
Score candidates
Select the best recommendation
Explain why that plan wins


without using an LLM for numerical decision making.

1. Phase Definition
Phase Name

Intervention Optimization Engine

Primary Goal

Determine the optimal recovery action from a set of simulated intervention candidates while respecting operational constraints and business objectives.

Core Question
Given multiple feasible recovery actions,
which one produces the best business outcome?

Required Result

For every simulation candidate:

Feasibility status
Constraint compliance
Recovery cost
Revenue protected
SLA breaches avoided
Delay reduction
Inventory impact
Supplier dependency impact
Operational risk score
Overall utility score
Relative ranking
Pareto position
Selection rationale

Core Transformation
Counterfactual Simulations
+
Business Objective
+
Business Constraints
+
Optimization Policy
↓
Feasibility Screening
↓
Metric Normalization
↓
Candidate Comparison
↓
Pareto Analysis
↓
Utility Evaluation
↓
Best Feasible Plan
↓
Recommendation Package
↓
Auditable Decision Record

2. Phase 7 Definition of Done

Phase 7 is complete only when:

Given multiple candidate intervention simulations, the system can deterministically identify all feasible plans, rank them using transparent scoring logic, generate a reproducible recommendation, explain the trade-offs, and persist a complete optimization audit trail.

3. Phase 7 Boundaries
In Scope

Feasibility validation

Constraint enforcement

Candidate comparison

Business scoring

Utility calculation

Pareto frontier generation

Dominance analysis

Sensitivity testing

Recommendation generation

Optimization audit records

Decision rationale

Benchmark evaluation

Policy versioning

Out Of Scope

Natural-language planning

LLM objective selection

LLM ranking

User conversation

Semantic evidence retrieval

Decision narration

These belong to Phases 8 and 9.

4. Phase Structure
Phase 7
├── 7A. Phase 6 Handoff Validation
├── 7B. Optimization Contract
├── 7C. Objective Model
├── 7D. Constraint Registry
├── 7E. Feasibility Validation Engine
├── 7F. Metric Extraction Layer
├── 7G. Normalization Engine
├── 7H. Utility Scoring Engine
├── 7I. Pareto Frontier Engine
├── 7J. Dominance Analysis
├── 7K. Recommendation Selection
├── 7L. Sensitivity Analysis
├── 7M. Decision Provenance
├── 7N. Persistence and Ledger
├── 7O. Golden Optimization Scenario
├── 7P. Benchmark Evaluation
├── 7Q. Performance Evaluation
├── 7R. Testing and Adversarial Validation
├── 7S. Observability
├── 7T. Independent Review Gate
└── 7U. Phase 8 Handoff

5. Phase 7A: Phase 6 Handoff Validation
Goal

Confirm optimization operates only on validated simulation outputs.

Required Inputs
Do-Nothing Scenario

Transfer Scenario

Expedite Scenario

Alternate Supplier Scenario

Reschedule Scenario

Hybrid Scenario


Each must include:

Result Hash

Revenue Risk

Delay

Breaches

Cost

Warnings

Feasibility Metadata

Provenance

Validation Checks
Scenario hashes valid

Simulation completed

Metrics available

Rule versions consistent

Candidate count ≥ 2

Deliverable
docs/optimization/phase-6-handoff-review.md

6. Phase 7B: Optimization Contract
Conceptual Signature
OptimizationResult optimize(
    CandidateResults simulations,
    OptimizationObjective objective,
    Constraints constraints,
    ScoringModel scoring
)

Deterministic Inputs
Simulation outputs

Constraint set

Objective

Weights

Scoring version

Must Not Depend On
LLM ranking

Random tie breaking

User interface order

Database retrieval order

Current time

Deliverable
docs/optimization/optimization-contract.md

7. Phase 7C: Objective Model

Objectives must be explicit.

Supported Objectives
MINIMIZE_REVENUE_RISK

MINIMIZE_SLA_BREACHES

MINIMIZE_DELAY

MINIMIZE_COST

MAXIMIZE_SERVICE_LEVEL

BALANCED_RECOVERY

Objective Object
{
  "objective":"BALANCED_RECOVERY",
  "weights":{
    "revenue":0.40,
    "sla":0.30,
    "cost":0.15,
    "delay":0.15
  }
}

Rule

Weights always sum to:

1.0

Deliverables
schemas/objective.schema.json

docs/optimization/objectives.md

8. Phase 7D: Constraint Registry

All constraints must be versioned exactly like rules.

Constraint Categories
Cost

Inventory

Supplier

Warehouse

Capacity

Delay

Regulatory

Example
constraint_id: CON-001

name: max_recovery_cost

value: 200000 INR

operator: <=

Typical Constraints
Recovery cost ≤ ₹2 lakh

Safety stock ≥ minimum

Supplier approved

Transfer lane approved

Delay ≤ 10 days

Capacity utilization ≤ 100%

Deliverable
config/constraints/

docs/optimization/constraint-catalogue.md

9. Phase 7E: Feasibility Validation Engine

Before scoring:

Check feasibility.

Invalid Plans Must Be Rejected

Examples:

Transfer violates safety stock

Supplier not approved

Expedite impossible

Capacity exceeded

Budget exceeded

Statuses
FEASIBLE

CONDITIONALLY_FEASIBLE

INFEASIBLE

Example
{
  "candidate":"TRANSFER",
  "status":"INFEASIBLE",
  "reason":"Safety stock violated"
}

Deliverable
src/backend/chronosdb/optimization/feasibility/

10. Phase 7F: Metric Extraction Layer

Extract optimization metrics.

Required Metrics

Revenue Risk

Revenue Protected

SLA Breaches

Breaches Avoided

Delay

Delay Reduction

Recovery Cost

Capacity Usage

Inventory Consumed

Remaining Inventory

Supplier Risk

Example
{
  "candidate":"HYBRID",
  "revenue_protected":1100000,
  "breaches_avoided":2,
  "delay_reduction_hours":240,
  "cost":132000
}

11. Phase 7G: Normalization Engine

Different units:

Rupees
Hours
Counts
Percentages


must become comparable.

Min-Max Normalization

Benefit Metric

(value-min)/(max-min)


Cost Metric

(max-value)/(max-min)


Normalized Range

0.0 → 1.0

Deliverable
src/backend/chronosdb/optimization/normalization/

12. Phase 7H: Utility Scoring Engine

Core optimization function.

Utility Formula

U

=
W1(SLA Saved)
+
W2(Revenue Protected)
-
W3(Cost)
-
W4(Remaining Delay)
-
W5(Operational Risk)


Recommended Default

Revenue Protected = 40%

SLA Saved = 30%

Cost = 15%

Delay = 10%

Risk = 5%

Example
Candidate	UtilityDo Nothing	0.00
Transfer	0.62
Expedite	0.73
Alternate Supplier	0.78
Hybrid	0.91
Output
{
  "candidate":"HYBRID",
  "utility_score":0.91
}

13. Phase 7I: Pareto Frontier Engine

One of the major differentiators.

Avoid assuming there is always one winner.

Example

Plan	Cost	Revenue ProtectedA	Low	Medium
B	Medium	High
C	High	Highest

All may be Pareto-optimal.

Output

PARETO_OPTIMAL

DOMINATED

Deliverable
src/backend/chronosdb/optimization/pareto/

14. Phase 7J: Dominance Analysis

Candidate A dominates B if:

A ≥ B on all objectives

AND

A > B on at least one objective


Example

B rejected

Reason:

Dominated by HYBRID plan


Useful later in UI.

15. Phase 7K: Recommendation Selection

Recommendation process:

Remove infeasible

Remove dominated

Generate Pareto set

Compute utilities

Select highest utility


Output

{
  "recommended_candidate":"HYBRID",
  "score":0.91,
  "rank":1
}

16. Phase 7L: Sensitivity Analysis

Extremely valuable for judges.

Question:

Would recommendation change
if priorities changed?


Test Variations

Cost Weight ±20%

SLA Weight ±20%

Revenue Weight ±20%

Delay Weight ±20%


Output

{
  "stable":true,
  "winner_changes":0
}


or

{
  "stable":false,
  "switches_to":"TRANSFER"
}

17. Phase 7M: Decision Provenance

Every recommendation must explain:

Example

Selected: HYBRID

Reason:

2 SLA breaches avoided

₹11 lakh revenue protected

Utility = 0.91

Cost = ₹1.32 lakh

Within all constraints

Pareto-optimal


Required Provenance

Candidate IDs

Metric Values

Weights

Constraint Results

Rule Versions

Simulation Hashes

18. Phase 7N: Persistence and Optimization Ledger

Records

OPTIMIZATION_RUN

OPTIMIZATION_INPUT

CANDIDATE_SCORE

CONSTRAINT_RESULT

PARETO_RESULT

RECOMMENDATION

SENSITIVITY_RESULT


Optimization Record

{
  "optimization_run_id":"OPT-001",
  "recommended_candidate":"HYBRID",
  "utility":0.91
}

19. Phase 7O: Golden Optimization Scenario

Locked Scenario

Candidates

Do Nothing

Transfer

Expedite

Alternate Supplier

Hybrid


Expected Winner

For your golden dataset:

Hybrid


Expected Metrics

Revenue Risk ↓

Revenue Protected ↑

Breaches ↓

Delay ↓

Cost within ₹2 lakh


Golden Requirement

Winner must exactly match frozen expected result.

20. Phase 7P: Benchmark Evaluation

Optimization Metrics

Feasibility Accuracy
Target 100%

Utility Fidelity
Target 100%

Constraint Accuracy
Target 100%

Pareto Accuracy
Target ≥98%

Recommendation Accuracy
Target ≥90%


against benchmark-optimal plan.

21. Phase 7Q: Performance
Operation	p95Feasibility	<100 ms
Utility Calculation	<100 ms
Pareto Construction	<200 ms
Optimization	<500 ms
Sensitivity Analysis	<2 sec
22. Phase 7R: Adversarial Testing

Required Tests

Impossible budget

Negative weights

Weights > 1.0

Missing revenue value

Duplicate scenario

Conflicting constraints

All candidates infeasible

Single candidate only

Identical scoring candidates

Tie conditions


Expected Behavior

Typed errors

Stable results

No crashes

Auditable failure

23. Phase 7S: Observability

Required Metrics

Candidates Evaluated

Candidates Rejected

Pareto Size

Winning Score

Constraint Violations

Optimization Runtime

24. Phase 7T: Independent Review Gate

Domain Review

Feasible plans remain feasible

No hidden assumptions

Costs calculated correctly


Optimization Review

Weights visible

Ranking reproducible

Pareto correct

Dominance valid


Audit Review

Recommendation traceable

Utility reproducible

Constraint evaluation visible


Judge Review

Can answer:

"Why this plan?"

within 10 seconds.

25. Phase 7 Scorecard
Category	WeightFeasibility Validation	15
Constraint Handling	10
Metric Extraction	10
Utility Scoring	15
Pareto Analysis	10
Recommendation Quality	15
Sensitivity Analysis	8
Provenance	7
Testing	5
Determinism	5
Performance	5
Total	100
Phase 7 Final Gate Checklist
Inputs

✅ Phase 6 outputs validated
 ✅ Rule versions pinned
 ✅ Candidate hashes verified

Feasibility

✅ Infeasible plans rejected
 ✅ Constraints enforced
 ✅ Safety stock respected

Optimization

✅ Utility scores correct
 ✅ Ranking stable
 ✅ Recommendation deterministic

Pareto

✅ Pareto frontier generated
 ✅ Dominance correct

Provenance

✅ Recommendation explainable
 ✅ Utility traceable
 ✅ Inputs recorded

Benchmark

✅ Golden optimization passes
 ✅ Recommendation agreement target met

Performance

✅ Optimization <500ms p95

Reliability

✅ All tests pass
 ✅ No severity-1 defects
 ✅ No automatic-failure condition remains

Phase 7U: Phase 8 Handoff

Phase 8 receives:

Chosen Recommendation

Candidate Rankings

Utility Scores

Pareto Frontier

Constraint Results

Sensitivity Results

Optimization Audit Trail


Phase 8 then answers:

"What evidence supports this recommendation?"

using:

Db2 Vector Retrieval
Historical Incidents
SOPs
Recovery Procedures
Supplier Notices
Structured Evidence

Final Phase 7 Outcome

When Phase 7 passes, ChronosDB completes Milestone M2: Decision Engine Complete.

The locked deliverable becomes:

chronosdb-optimization-engine-v1.0.0


ChronosDB can now:

Detect disruption
↓
Calculate impact
↓
Simulate alternatives
↓
Compare outcomes
↓
Select best recovery plan
↓
Prove why it is best


At this point, the core competitive differentiator is fully operational:

ChronosDB does not merely predict disruption impact. It evaluates multiple futures and deterministically selects the best feasible response under real business constraints.