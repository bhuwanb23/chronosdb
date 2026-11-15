Phase 6 Deep Dive: Counterfactual Simulation Engine
Simulate Alternative Futures Without Mutating Operational Reality

Phase 5 answered:

"What happens if the disruption occurs and we do nothing?"

Phase 6 answers:

"Given the exact same disrupted world, what would happen if we intervened differently?"

This is the phase where ChronosDB stops being an impact-analysis system and becomes a decision-intelligence platform.

The most important architectural rule of Phase 6 is:

No intervention is allowed to modify operational truth.

Every simulation must run against:

Same baseline state
Same reconstructed state
Same supplier outage
Same simulation horizon
Same rule set
Same scheduling policies

Only intervention changes


That is what makes counterfactual comparison scientifically valid and auditable.

1. Phase Definition
Phase Name

Counterfactual Simulation Engine

Primary Goal

Implement an isolated scenario simulation framework capable of applying intervention overlays to a disrupted operational state and calculating their impact using the deterministic Phase 5 impact engine.

Core Question
What happens if we take action X
instead of doing nothing?


where X may be:

Inventory transfer
Purchase-order expedition
Alternate supplier activation
Production rescheduling
Hybrid multi-action recovery

Required Result

For every intervention scenario ChronosDB must deterministically calculate:

Modified supply events
Modified inventory timelines
Modified shortages
Modified production schedules
Modified customer fulfilment
Modified SLA exposure
Modified revenue at risk
Intervention cost
Operational side effects
Comparison against baseline


while preserving:

Original operational state
Original disruption
Original Phase 5 output

Core Transformation
Frozen Operational State
+
Supplier Outage
+
Intervention Overlay
+
Rule Version
+
Simulation Horizon
↓
Modified Supply
↓
Modified Inventory
↓
Modified Production
↓
Modified Customer Impact
↓
Modified SLA Impact
↓
Modified Revenue Risk
↓
Comparison Against Do-Nothing Baseline
↓
Auditable Counterfactual Result

2. Phase 6 Definition of Done

Phase 6 is complete only when:

Given the same disrupted state and deterministic rules, the system can simulate multiple isolated intervention candidates, produce repeatable outcomes, compare them against the do-nothing baseline, and persist all results with complete traceability.

3. Phase 6 Boundaries
In Scope

Scenario overlays

Warehouse transfer simulation

Purchase-order expedition simulation

Alternate supplier simulation

Production rescheduling simulation

Combined interventions

Scenario isolation

Delta calculation

Impact comparison

Simulation persistence

Counterfactual causality

Scenario replay

Intervention costs

Feasibility validation

Simulation benchmarking

Repeatability testing

Out Of Scope

Intervention ranking

Optimization

Pareto frontiers

Sensitivity analysis

LLM-generated interventions

Natural language planning

Recommendation selection

Multi-objective optimization

These belong to Phase 7.

4. Phase Structure
Phase 6
├── 6A. Phase 5 Handoff Validation
├── 6B. Simulation Contract and Boundaries
├── 6C. Scenario and Overlay Model
├── 6D. Intervention Registry
├── 6E. Scenario Baseline Construction
├── 6F. Inventory Transfer Simulator
├── 6G. Purchase Order Expedition Simulator
├── 6H. Alternate Supplier Simulator
├── 6I. Production Rescheduling Simulator
├── 6J. Hybrid Intervention Simulator
├── 6K. Overlay Application Engine
├── 6L. Simulation Execution Engine
├── 6M. Delta Computation Engine
├── 6N. Counterfactual Causality
├── 6O. Persistence and Scenario Ledger
├── 6P. Determinism and Replay
├── 6Q. Golden Intervention Scenarios
├── 6R. Benchmark Evaluation
├── 6S. Performance Evaluation
├── 6T. Testing and Adversarial Validation
├── 6U. Observability
├── 6V. Independent Review Gate
└── 6W. Phase 7 Handoff

5. Phase 6A: Phase 5 Handoff Validation
Goal

Verify that Phase 6 receives a frozen deterministic baseline.

Required Inputs
chronosdb-impact-engine-v1.0.0

golden-impact-result.json

impact benchmark report

impact rule manifest

state hash manifest

causal trace schema

determinism report

Required Validation
Phase 5 rule version exists

Golden state hash exists

Golden result hash exists

Golden revenue-at-risk exists

Golden SLA counts exist

No benchmark corruption

Deliverables
docs/simulation-engine/phase-5-handoff-review.md

Exit Gate
Impact engine reproducible

State hashes valid

Rule versions frozen

Golden results frozen

Simulation cannot mutate baseline records

6. Phase 6B: Simulation Contract
Conceptual Signature
SimulationResult simulate(
    OperationalState state,
    Disruption disruption,
    InterventionOverlay overlay,
    RuleSet rules,
    Horizon horizon
)

Deterministic Inputs

Must depend only on:

state hash

disruption definition

overlay definition

horizon

rule set

allocation policy

scheduling policy

Must Not Depend On
current time

thread scheduling

randomness

LLM output

network requests

user interface state

Deliverable
docs/simulation-engine/simulation-contract.md

7. Phase 6C: Scenario and Overlay Model

The core ChronosDB architectural innovation.

Instead of:

Change operational database


we do:

State
+
Overlay
=
Simulation State

Overlay Categories
Inventory Overlay
{
  "action":"TRANSFER_INVENTORY",
  "component_id":"CMP-MCU-42",
  "quantity":"320",
  "from_warehouse":"WH-CHENNAI",
  "to_warehouse":"WH-PUNE"
}

Expedition Overlay
{
  "action":"EXPEDITE_PO",
  "purchase_order_id":"PO-2208",
  "lead_time_reduction_days":5
}

Alternate Supplier Overlay
{
  "action":"ACTIVATE_ALT_SUPPLIER",
  "supplier_id":"SUP-0208",
  "component_id":"CMP-MCU-42",
  "available_quantity":"300"
}

Reschedule Overlay
{
  "action":"RESCHEDULE_PRODUCTION",
  "production_order_id":"MO-0882",
  "priority":1
}

Deliverables
schemas/simulation-overlay.schema.json

docs/simulation-engine/overlay-model.md

8. Phase 6D: Intervention Registry

Exactly as Phase 5 used Rule Registry.

Simulation actions must be versioned.

Intervention Types
INT-TRANSFER
INT-EXPEDITE
INT-SUPPLIER
INT-RESCHEDULE
INT-HYBRID


Example

intervention_id: INT-TRANSFER
version: 1.0.0

inputs:
  component_id
  quantity
  source_warehouse
  destination_warehouse

validation:
  transferable_inventory > quantity
  remaining_after_transfer >= safety_stock

Deliverables
config/interventions/

docs/simulation-engine/intervention-catalogue.md

9. Phase 6E: Scenario Baseline Construction

Every simulation starts from:

Phase 5 State
+
Phase 5 Disruption


NOT from live data.

Simulation baseline:

{
  "baseline_id":"BASE-GOLD-001",
  "state_hash":"...",
  "impact_run_id":"IR-001",
  "revenue_at_risk":"1600000",
  "sla_breaches":2
}

Identity Rule

Every candidate must share:

same state hash

same disruption

same horizon

same rule set


Only overlay differs.

10. Phase 6F: Inventory Transfer Simulator

Simulate:

Chennai → Pune


without changing warehouse inventory records.

Transfer Validation

Source inventory exists

Above safety stock

Transfer lane valid

Arrival inside horizon

Quantity positive


Generated Event

{
  "event_type":"SIM_TRANSFER_RECEIPT",
  "component_id":"CMP-MCU-42",
  "quantity":"320",
  "arrival_time":"2026-11-14T00:00:00Z"
}


Impact

Earlier material availability

Reduced shortage

Reduced delay

11. Phase 6G: Expedition Simulator

Goal:

Bring supply earlier.

Example

Phase 5

PO-2208
27 Nov


Expedite

PO-2208
22 Nov


Constraints

cannot precede shipment release

cannot exceed supplier capability

must incur expedition cost


Cost Model

Expedition Cost

=
base freight
+
premium freight
+
supplier surcharge

12. Phase 6H: Alternate Supplier Simulator

Create new projected supply.

Example

SUP-0208

300 MCU

Lead time = 3 days


Validation

approved component

active agreement

supplier capacity available


Generated Event

SIM_ALT_SUPPLIER_RECEIPT

13. Phase 6I: Production Rescheduling

No supply changes.

Only sequencing changes.

Example

Before

MO-0876
MO-0882
MO-0889


After

MO-0882
MO-0876
MO-0889


Outputs

priority changes

delay shifts

customer impact shifts

14. Phase 6J: Hybrid Intervention Simulator

Multiple overlays.

Example:

Transfer Inventory
+
Alternate Supplier
+
Reschedule Production


Rules

Apply overlays in deterministic order

Transfer
→ Supplier
→ Expedition
→ Reschedule


Stable ordering required.

15. Phase 6K: Overlay Application Engine

Core algorithm.

Input

Phase 5 Baseline
Overlay


Output

Simulation State


Architecture

Load Baseline

Apply Virtual Changes

Generate Overlay Events

Recompute Derived State


No operational records modified.

Ever.

16. Phase 6L: Simulation Execution Engine

Pipeline

Load Baseline

Apply Overlay

Execute Phase 5 Engine

Capture Results

Persist Outcomes


Critical Principle

Do not rewrite:

inventory logic

allocation logic

scheduling logic

financial logic


Reuse Phase 5.

Phase 6 becomes:

State Modifier
+
Impact Engine Runner

17. Phase 6M: Delta Computation Engine

Compute savings.

Revenue Protected

Revenue Protected

=
DoNothing Revenue Risk
-
Scenario Revenue Risk


Breaches Avoided

Breaches Avoided

=
DoNothing Breaches
-
Scenario Breaches


Delay Reduction

Delay Reduction

=
DoNothing Delay
-
Scenario Delay


Example

Metric	Baseline	TransferRevenue Risk	₹1.6M	₹0.8M
Breaches	2	1
Delay	288 h	120 h

Derived

Revenue Protected = ₹800k

Breaches Avoided = 1

Delay Reduced = 168h

18. Phase 6N: Counterfactual Causality

Phase 5:

Why was impact created?


Phase 6:

Why was impact reduced?


Example

Transfer
↓
Inventory Available Earlier
↓
MO-0882 Starts Earlier
↓
CO-0704 Delivered On Time
↓
Revenue Protected ₹800k


New causal edge types

MITIGATES

AVOIDS_BREACH

PROTECTS_REVENUE

RESTORES_SUPPLY

ACCELERATES

19. Phase 6O: Persistence and Scenario Ledger

Required records

SIMULATION_RUN

SIMULATION_INPUT

SIMULATION_ACTION

SIMULATION_RESULT

SIMULATION_DELTA

SIMULATION_WARNING

SIMULATION_ERROR


Simulation Record

{
  "simulation_run_id":"SIM-001",
  "baseline_run_id":"IR-001",
  "overlay_hash":"...",
  "result_hash":"...",
  "runtime_ms":945
}

20. Phase 6P: Determinism and Replay

Run:

Golden Transfer Scenario

100 times


Target

Unique business outputs = 1


Benchmark

20 scenarios

10 reruns each

200 stable outputs


Replay

Restart

Re-run

Cross-process

Cross-host


Same result.

21. Phase 6Q: Golden Intervention Scenarios

Required locked scenarios.

GI-001

Inventory Transfer

GI-002

Purchase Expedition

GI-003

Alternate Supplier

GI-004

Reschedule Production

GI-005

Hybrid Recovery

Each scenario must define:

Expected shortages

Expected delays

Expected SLA breaches

Expected revenue

22. Phase 6R: Benchmark Evaluation

Metrics

Simulation Fidelity
Target: 100%

Delta Accuracy
Target: 100%

Overlay Isolation
Target: 100%

Replay Stability
Target: 100%

Scenario Completeness
Target: 100%

23. Phase 6S: Performance

Target P95

Operation	TargetOverlay Build	<100 ms
Transfer Simulation	<300 ms
Supplier Simulation	<500 ms
Full Scenario	<2.5 sec
Comparison Generation	<300 ms
24. Phase 6T: Adversarial Tests

Required fixtures

Negative transfer quantity

Transfer exceeds available stock

Transfer violates safety stock

Unknown alternate supplier

Expedite impossible PO

Invalid priority

Broken overlay

Duplicate intervention

Conflicting intervention

Expired agreement


Expected behavior

Validation failure

No simulation executed

Typed errors returned

Baseline remains unchanged

25. Phase 6V: Release Gate

Phase 6 passes only when:

Functional
Inventory transfer works
Expedition works
Alternate supplier works
Reschedule works
Hybrid works
Integrity
Baseline never changes
Overlay isolated
Repeated execution identical
Financial
Revenue protection calculated correctly
Breaches avoided calculated correctly
Delay reduction calculated correctly
Auditability
Every benefit has causal evidence
Every simulation has provenance
Every result has hashes
Performance
P95 within targets
Quality
Golden intervention suite passes
No severity-1 defects
No flaky tests
26. Phase 6W: Phase 7 Handoff

Phase 7 receives:

Do-Nothing Result

Transfer Result

Expedite Result

Alternate Supplier Result

Reschedule Result

Hybrid Result


with:

Revenue Risk
Breaches
Delay
Cost
Warnings
Feasibility
Provenance
Result Hash

Required Phase 7 Calculations

Phase 7 must compute:

RevenueProtected_i
=
RevenueRisk_baseline
-
RevenueRisk_i

BreachesAvoided_i
=
Breaches_baseline
-
Breaches_i

DelayReduction_i
=
Delay_baseline
-
Delay_i

Utility_i
=
w1(SLA Saved)
-
w2(Cost)
-
w3(Delay)
-
w4(Risk)

Final Phase 6 Outcome

When Phase 6 passes, ChronosDB gains its first genuinely unique capability:

Not:
"What happened?"

Not:
"What will happen?"

But:

"What would happen if we act differently?"


The locked deliverable becomes:

chronosdb-counterfactual-engine-v1.0.0


And Milestone M2 becomes approximately 80% complete, with only Phase 7 (Optimization Engine) remaining before the full Decision Engine milestone is closed.