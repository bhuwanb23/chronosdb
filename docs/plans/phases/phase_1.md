Phase 1 Deep Dive: Product and Judging Specification

You have completed Phase 0, so we now treat the repository, environment, IBM Db2 connectivity, compliance controls, and engineering baseline as stable. Phase 1 converts the locked ChronosDB concept into a testable product contract so that Phase 2 can model the supply-chain domain without ambiguity.

Phase 1 is where we decide precisely:

Who ChronosDB is for
What operational decision it improves
What the system must and must not do
What outputs count as correct
How every feature contributes to the judging rubric
How success will be measured
Which requirements later phases must implement and test
1. Phase 1 purpose
Phase name

Product, User, Requirements and Judging Specification

Primary goal

Convert ChronosDB from a strong idea into a complete, testable specification for an auditable supply-chain decision system.

Required result

At the end of Phase 1, another engineer should be able to read the specification and know:

The exact user and problem.
The exact workflow.
The exact inputs and outputs.
The exact MVP boundary.
Which outputs are deterministic.
Which outputs may use an LLM.
What every important business term means.
How every requirement will be tested.
How every feature maps to the judging criteria.
What Phase 2 must model.
Phase 1 is not

Phase 1 is not the stage for:

Designing database tables
Generating the synthetic dataset
Implementing the simulator
Writing the optimization algorithm
Creating prompts
Building the dashboard
Selecting UI colors
Claiming accuracy
Implementing speculative features

Those activities belong to later phases.

2. Phase 1 structure
Phase 1
├── 1A. Phase 0 handoff validation
├── 1B. Product identity and narrative lock
├── 1C. Stakeholder and user specification
├── 1D. Problem and decision specification
├── 1E. End-to-end user journey
├── 1F. Use-case catalogue
├── 1G. Functional requirements
├── 1H. Non-functional requirements
├── 1I. Data and evidence requirements
├── 1J. AI authority and control specification
├── 1K. MVP and scope control
├── 1L. Judging-rubric alignment
├── 1M. Success metrics and evaluation contract
├── 1N. Acceptance-test specification
├── 1O. Risks, assumptions and unresolved questions
├── 1P. Requirements review and quality benchmark
└── 1Q. Phase 2 handoff

3. Phase 1A: Phase 0 handoff validation
Goal

Confirm that Phase 1 starts from an actual foundation rather than assumptions.

Inputs required from Phase 0

Verify the existence of:

Product charter
Submission requirement register
Compliance matrix
Decision log
Risk register
Assumption register
Version matrix
Db2 capability report
Foundation benchmark
Phase 0 completion report
Foundation commit hash or tag
Handoff checks
Check	Required resultProject name	ChronosDB
Primary domain	Supply-chain disruption intelligence
Primary scenario	Critical supplier outage
Primary database	IBM Db2
AI framework	LangChain
Backend	Python and FastAPI
Calculation authority	Deterministic Python and SQL
LLM authority	Interpretation and explanation only
Foundation tests	Passing
Critical Phase 0 risks	Zero untreated
Deliverable
docs/product/phase-0-handoff-review.md

Exit gate

Phase 1A passes when:

Every required input exists.
No decision contradicts the locked architecture.
Any deferred Phase 0 issue has an owner.
The product scope remains a supplier-outage vertical slice.
No major technical uncertainty prevents requirements definition.
4. Phase 1B: Product identity and narrative lock
Goal

Create one product description used consistently in the repository, architecture, application and demo.

Locked identity
Product name
ChronosDB
Descriptive title

ChronosDB: Auditable Counterfactual Intelligence for Supply-Chain Disruptions

Category

Db2-native operational decision intelligence

Primary tagline

Reconstruct the past. Simulate the future. Prove the decision.

One-sentence description

ChronosDB helps supply-chain operations managers understand the cascading impact of a supplier disruption, compare feasible recovery interventions, and verify every recommendation using evidence stored in IBM Db2.

Thirty-second description

When a critical supplier fails, normal dashboards show the immediate delay but not the full operational cascade. ChronosDB reconstructs the current supply-chain state from IBM Db2, calculates which components, production orders and customer commitments are affected, simulates recovery options, and recommends the best feasible action under cost and service constraints. Every result links back to the database records and calculation rules that produced it.

Product promise

ChronosDB must answer five questions:

What happened?
What will be affected?
What happens if we do nothing?
Which interventions are feasible?
Why is the recommended intervention preferable?
Product differentiator

ChronosDB is not an AI chatbot that guesses what might happen. It is a deterministic decision simulator with an AI-assisted interface and a Db2-backed evidence trail.

Narrative constraints

Avoid these claims unless later validated:

“Digital twin of the entire enterprise”
“Predicts the future”
“Zero hallucinations”
“Perfect accuracy”
“Real-time ERP integration”
“Autonomous supply-chain management”
“Guaranteed optimal decision”
“Prevents every disruption”

Use these defensible alternatives:

“Scenario-based operational model”
“Projects counterfactual outcomes”
“Verifies numerical claims”
“Measures accuracy against benchmark scenarios”
“Uses reproducible synthetic operational data”
“Recommends interventions for human review”
Deliverable
docs/product/product-identity.md

Exit gate

Every project-facing description must use the same:

Name
User
Problem
Core scenario
Product promise
Differentiator
Capability boundaries
5. Phase 1C: Stakeholder and user specification
Goal

Define who uses ChronosDB, who depends on its outputs, and which needs take priority.

5.1 Primary user
Supply-chain operations manager

The primary user is responsible for:

Monitoring supplier disruptions
Protecting production continuity
Managing inventory allocation
Coordinating warehouses and production facilities
Protecting customer service-level commitments
Controlling recovery expenditure
Explaining recovery decisions to management
Primary-user goals

The user needs to:

Understand the consequence of a disruption quickly.
Identify the operational bottleneck.
Compare recovery alternatives.
Ensure each alternative is feasible.
Balance service impact against cost.
Explain the recommendation to leadership.
Preserve a record of why the decision was made.
Primary-user pain points
Data is split across suppliers, inventory, production and orders.
Immediate disruption impact is visible, but downstream impact is not.
Spreadsheet analysis is slow and difficult to reproduce.
AI-generated recommendations may contain unsupported numbers.
Recovery options may violate inventory or supplier constraints.
Decisions are difficult to audit after the event.
5.2 Secondary stakeholders
Production planner

Needs:

Component availability
Production-order impact
Rescheduling possibilities
Facility capacity consequences
Procurement analyst

Needs:

Alternate supplier availability
Lead-time changes
Supply cost
Supplier qualification status
Warehouse manager

Needs:

Transferable inventory
Safety-stock constraints
Transfer timing
Source-warehouse impact
Customer-service manager

Needs:

Affected customer orders
Promised dates
Projected delay
SLA exposure
Finance or business manager

Needs:

Revenue at risk
Recovery cost
Revenue protected
Trade-off explanation
Auditor or risk reviewer

Needs:

Scenario inputs
Source records
Rule versions
Candidate interventions
Final recommendation
Timestamps and decision history
5.3 User-priority hierarchy

When stakeholder goals conflict, ChronosDB should use this default priority:

Data integrity and intervention feasibility
Committed customer service level
Production continuity
Revenue protection
Recovery cost
Convenience or narrative quality

This ordering is a product default, not an immutable business rule. Later phases should make optimization weights configurable.

5.4 User-persona specification

Create one detailed primary persona.

Example persona
Name: Ananya Rao
Role: Regional Supply-Chain Operations Manager
Organization type: Electronics manufacturer
Responsibilities:
- 2 production facilities
- 3 warehouses
- 20 active suppliers
- 500 open customer orders

Typical disruption:
A critical microcontroller supplier reports a 14-day delay.

Current process:
ERP exports + spreadsheets + calls to procurement and production.

Current decision time:
Approximately 2–6 hours for a complex disruption.

Desired decision time:
First defensible scenario comparison within 5 minutes.


The persona is synthetic and must be labelled as such.

Deliverables
docs/product/stakeholder-map.md
docs/product/primary-persona.md
docs/product/user-needs.md

Benchmark
User-need coverage
UNC=primary user needs mapped to requirementstotal documented primary user needsUNC = \frac{\text{primary user needs mapped to requirements}} {\text{total documented primary user needs}}

Target:

UNC = 100%

6. Phase 1D: Problem and decision specification
Goal

Define the exact decision ChronosDB supports.

Core problem statement

When a critical supplier becomes unavailable, operational dependencies cause delayed components to propagate into inventory shortages, production delays, customer-order breaches and revenue exposure. Existing dashboards show isolated operational facts but do not consistently simulate alternative recovery actions or preserve an auditable explanation of the selected intervention.

Core decision

Given a supplier disruption, the current operational state, available interventions and business constraints, which feasible intervention produces the best service and financial outcome?

Decision inputs

The decision requires:

Disrupted supplier
Disruption start time
Disruption duration
Affected purchase orders
Component supply from that supplier
Current inventory
Reserved inventory
Expected consumption
Bill-of-material dependencies
Production schedule
Customer orders
Customer due dates
Customer priority
Supplier alternatives
Warehouse transfer availability
Intervention budget
Safety-stock rules
Facility capacity
Decision outputs

The system must return:

Baseline or do-nothing impact
Affected components
Component shortage quantities
Shortage dates
Affected production orders
Production delay days
Affected customer orders
Projected delivery dates
Projected SLA breaches
Revenue at risk
Intervention comparison

For each candidate:

Intervention type
Required actions
Feasibility status
Rejection reason, when infeasible
Additional cost
Projected delay
SLA breaches
Revenue at risk
Revenue protected relative to do nothing
Operational risks
Score or Pareto position
Supporting evidence
Recommendation
Selected intervention
Selection objective
Active constraints
Trade-offs
Evidence
Calculation version
Scenario run ID
Warnings
Human-review statement
6.1 Key decision distinction

ChronosDB does not make a procurement transaction. It provides a decision-support recommendation.

The user remains responsible for:

Approving the intervention
Contacting suppliers
Initiating warehouse transfers
Modifying production
Communicating with customers

This distinction reduces safety, governance and credibility risks.

6.2 Objective hierarchy

The application must support at least these objectives:

MINIMIZE_SLA_BREACHES
MINIMIZE_REVENUE_AT_RISK
MINIMIZE_TOTAL_DELAY
MINIMIZE_RECOVERY_COST
BALANCED_RECOVERY


The MVP demo should default to:

MINIMIZE_SLA_BREACHES


subject to:

maximum_recovery_cost
minimum_source_safety_stock
approved_supplier_only
facility_capacity
available_inventory

Deliverable
docs/product/decision-specification.md

Exit gate
The decision has defined inputs.
The decision has defined outputs.
The objective is explicit.
Constraints are separated from preferences.
Recommendations are not confused with autonomous actions.
Every numerical output has a future calculation owner.
7. Phase 1E: End-to-end user journey
Goal

Specify the complete user experience before APIs and screens are designed.

Journey stage 1: Select operational state

The user chooses:

Current operational state, or
Historical as-of timestamp
Result

ChronosDB identifies which version of supply-chain data should be used.

Failure cases
Timestamp predates available history
Required snapshot unavailable
Some records have conflicting effective dates
Journey stage 2: Define disruption

The user enters:

Event type: supplier outage
Supplier identifier
Start time
Duration
Optional affected purchase orders
Operational notes

Example:

Supplier S-104 is unavailable for 14 days beginning 11 November.

Result

A validated scenario request is created.

Failure cases
Supplier does not exist
Supplier has no active component relationship
Duration is negative
Start date is invalid
Required field is missing
Journey stage 3: Define constraints

The user enters:

Maximum recovery budget
Minimum service level
Safety-stock policy
Optimization objective
Optional intervention exclusions

Example:

Maximum recovery cost: ₹200,000
Objective: Minimize SLA breaches
Do not use unapproved suppliers

Journey stage 4: Create immutable scenario

ChronosDB stores:

Scenario inputs
Operational-state reference
Constraint set
User-selected objective
Creation time
Scenario ID
Rule version

Once simulation begins, the original scenario input cannot be silently changed.

Journey stage 5: Calculate do-nothing impact

ChronosDB calculates the consequence of taking no intervention.

The user sees:

Dependency cascade
Shortage timeline
Affected production orders
Affected customer orders
SLA exposure
Revenue at risk
Journey stage 6: Generate candidate interventions

ChronosDB creates candidates such as:

Do nothing
Transfer inventory from another warehouse
Expedite an existing shipment
Use an approved alternate supplier
Reschedule production
Use a hybrid recovery plan
Journey stage 7: Validate candidates

Each candidate is checked against:

Available quantity
Warehouse safety stock
Supplier approval
Supplier capacity
Budget
Transfer time
Production capacity
Planning horizon

An infeasible candidate remains visible with its rejection reason.

This is better than silently deleting it because judges can see the constraint reasoning.

Journey stage 8: Simulate candidates

For every feasible intervention, ChronosDB calculates:

New inventory projection
New production completion
New customer delivery projection
New SLA count
New revenue-at-risk value
Additional cost
Journey stage 9: Compare alternatives

The user compares:

Do nothing
Cheapest intervention
Best service-level intervention
Lowest-delay intervention
Balanced recommendation
Journey stage 10: Review recommendation

ChronosDB explains:

Why the intervention was selected
Which constraints affected selection
Which outcome improved
What additional cost is required
Which risks remain
Which evidence was used
Journey stage 11: Inspect evidence

The user can open:

Source Db2 records
Calculation trace
Historical incident
Relevant operating procedure
Rule version
Simulation run
Decision audit record
Journey stage 12: Replay decision

The user can move through:

Initial operational state
Disruption introduced
Baseline impact
Candidate generation
Candidate simulation
Recommendation
Final audit snapshot
Deliverable
docs/product/end-to-end-user-journey.md

Benchmark

Every journey step must map to:

At least one functional requirement
At least one success condition
At least one failure behavior
At least one future test

Target coverage:

100%

8. Phase 1F: Use-case catalogue
Goal

Create formal use cases with preconditions, triggers, flows and outcomes.

UC-001: Create supplier-outage scenario
Actor

Supply-chain operations manager

Preconditions
Supplier exists.
Operational data is available.
User has scenario-creation permission.
Trigger

User creates a supplier-outage scenario.

Main flow
User selects supplier.
User enters start time and duration.
User selects objective.
User adds constraints.
System validates values.
System creates scenario.
System returns scenario ID.
Alternate flows
Unknown supplier
Invalid duration
Missing objective
Unsatisfiable constraint
Historical state unavailable
Postcondition

An immutable scenario exists.

UC-002: Calculate the do-nothing impact
Preconditions
Valid scenario exists.
Required supply-chain records are available.
Main flow
System loads scenario state.
System determines affected components.
System projects inventory shortages.
System calculates production effects.
System calculates customer-order effects.
System records the result.
System presents calculation evidence.
Postcondition

A reproducible baseline outcome exists.

UC-003: Generate intervention candidates

Candidate set:

Inventory transfer
Shipment expedition
Alternate supplier
Production rescheduling
Hybrid intervention
Postcondition

Every candidate is marked:

FEASIBLE
INFEASIBLE
INSUFFICIENT_DATA

UC-004: Compare intervention outcomes

The system presents comparable metrics using the same units and baseline.

UC-005: Recommend an intervention

The system selects the highest-ranking feasible candidate under the selected objective.

UC-006: Inspect evidence

The user can follow each major result to its source records and calculation trace.

UC-007: Replay an earlier decision

The user can load a completed scenario without recomputing or changing its original result.

UC-008: Handle insufficient data

The system must distinguish:

NO_IMPACT
NO_FEASIBLE_INTERVENTION
INSUFFICIENT_DATA
SIMULATION_FAILED


These are not equivalent states.

UC-009: Operate without LLM service

The system must still:

Accept a structured scenario
Run deterministic calculations
Compare interventions
Display a templated summary
Preserve evidence

Natural-language parsing and narration may be unavailable.

Deliverable
docs/product/use-case-catalogue.md

Exit criteria

Each use case contains:

ID
Actor
Preconditions
Trigger
Main flow
Alternate flows
Failure behavior
Postconditions
Related requirements
Future test IDs
9. Phase 1G: Functional requirements
Goal

Create atomic, testable product requirements.

Use requirement language consistently:

SHALL means mandatory.
SHOULD means important but deferrable.
MAY means optional.
Avoid “smart,” “easy,” “fast,” or “accurate” without a metric.
9.1 Scenario-management requirements
FR-SCN-001

The system SHALL create a supplier-outage scenario from structured input.

FR-SCN-002

The system SHALL assign a unique scenario identifier.

FR-SCN-003

The system SHALL store the scenario creation timestamp.

FR-SCN-004

The system SHALL validate the supplier against active supplier records.

FR-SCN-005

The system SHALL reject non-positive disruption durations.

FR-SCN-006

The system SHALL store the selected optimization objective.

FR-SCN-007

The system SHALL store all user-defined constraints.

FR-SCN-008

The system SHALL preserve the exact operational-state reference used for the scenario.

FR-SCN-009

The system SHALL NOT silently modify scenario inputs after execution begins.

FR-SCN-010

The system SHALL permit a user to duplicate an existing scenario into a new scenario.

9.2 Impact-analysis requirements
FR-IMP-001

The system SHALL determine the components supplied by the disrupted supplier.

FR-IMP-002

The system SHALL determine which expected replenishments are affected.

FR-IMP-003

The system SHALL project available inventory over the simulation horizon.

FR-IMP-004

The system SHALL calculate the earliest shortage date for every affected component.

FR-IMP-005

The system SHALL calculate the projected shortage quantity.

FR-IMP-006

The system SHALL identify products whose bills of material depend on affected components.

FR-IMP-007

The system SHALL identify affected production orders.

FR-IMP-008

The system SHALL calculate projected production-order delay.

FR-IMP-009

The system SHALL identify affected customer orders.

FR-IMP-010

The system SHALL calculate projected customer delivery dates.

FR-IMP-011

The system SHALL classify projected SLA status.

FR-IMP-012

The system SHALL calculate revenue at risk using a documented rule.

FR-IMP-013

The system SHALL preserve intermediate calculation values.

FR-IMP-014

The system SHALL produce a do-nothing baseline for every valid scenario.

9.3 Intervention requirements
FR-INT-001

The system SHALL create a do-nothing candidate.

FR-INT-002

The system SHALL evaluate inventory transfer where transferable stock exists.

FR-INT-003

The system SHALL evaluate expedition of eligible purchase orders.

FR-INT-004

The system SHALL evaluate approved alternate suppliers.

FR-INT-005

The system SHALL evaluate production rescheduling.

FR-INT-006

The system SHOULD evaluate at least one hybrid intervention.

FR-INT-007

The system SHALL preserve infeasible candidates and rejection reasons.

FR-INT-008

The system SHALL detect violations of minimum safety stock.

FR-INT-009

The system SHALL detect violations of the recovery budget.

FR-INT-010

The system SHALL reject unapproved supplier substitution.

FR-INT-011

The system SHALL calculate intervention cost using documented components.

9.4 Simulation requirements
FR-SIM-001

The system SHALL simulate each feasible intervention against the same baseline state.

FR-SIM-002

The system SHALL NOT mutate baseline operational records.

FR-SIM-003

The system SHALL assign a unique simulation-run identifier.

FR-SIM-004

The system SHALL record the calculation-rule version.

FR-SIM-005

The system SHALL record simulation warnings and errors.

FR-SIM-006

The system SHALL produce identical results for the same input state and rule version.

FR-SIM-007

The system SHALL prevent scenarios from contaminating one another.

9.5 Optimization requirements
FR-OPT-001

The system SHALL rank only feasible interventions.

FR-OPT-002

The system SHALL rank candidates according to the selected objective.

FR-OPT-003

The system SHALL expose the objective and weights used.

FR-OPT-004

The system SHALL expose the constraints applied.

FR-OPT-005

The system SHALL identify ties.

FR-OPT-006

The system SHALL return NO_FEASIBLE_INTERVENTION when no candidate satisfies the constraints.

FR-OPT-007

The system SHALL provide a reason for the selected intervention.

FR-OPT-008

The system SHOULD expose Pareto-efficient candidates when objectives conflict.

9.6 Evidence requirements
FR-EVD-001

The system SHALL associate every major numerical claim with a simulation run.

FR-EVD-002

The system SHALL identify the source records used by major calculations.

FR-EVD-003

The system SHALL store the calculation rule version.

FR-EVD-004

The system SHALL retrieve relevant historical incidents.

FR-EVD-005

The system SHALL retrieve relevant operating procedures.

FR-EVD-006

The system SHALL preserve document version and chunk identity for retrieved evidence.

FR-EVD-007

The system SHALL distinguish database facts from retrieved documents.

FR-EVD-008

The system SHALL indicate when supporting evidence is unavailable.

FR-EVD-009

The system SHALL NOT fabricate an evidence link.

9.7 Explanation requirements
FR-EXP-001

The system SHALL explain the do-nothing impact.

FR-EXP-002

The system SHALL explain why the recommended intervention was selected.

FR-EXP-003

The system SHALL explain the primary trade-off.

FR-EXP-004

The system SHALL expose remaining risks.

FR-EXP-005

The system SHALL verify generated numerical statements against structured outputs.

FR-EXP-006

The system SHALL remove or reject unsupported numerical statements.

FR-EXP-007

The system SHALL provide a deterministic summary if the LLM is unavailable.

9.8 Audit requirements
FR-AUD-001

The system SHALL record scenario creation.

FR-AUD-002

The system SHALL record each simulation run.

FR-AUD-003

The system SHALL record candidate feasibility decisions.

FR-AUD-004

The system SHALL record the selected recommendation.

FR-AUD-005

The system SHALL record model calls used for planning or narration.

FR-AUD-006

The system SHALL record verification results.

FR-AUD-007

The system SHALL allow a completed decision to be replayed.

FR-AUD-008

The normal application role SHALL NOT modify historical audit records.

Functional requirement deliverable
docs/product/functional-requirements.md

Requirement-quality gate

Every functional requirement must be:

Atomic
Necessary
Unambiguous
Implementation-neutral where possible
Testable
Traceable to a user need
Traceable to a use case
Assigned a priority
10. Phase 1H: Non-functional requirements
Goal

Define how well the system must operate.

10.1 Correctness
NFR-COR-001

For the frozen golden scenario, deterministic results must exactly match the approved expected outcomes.

NFR-COR-002

Numerical fidelity must be 100% for displayed deterministic values.

NFR-COR-003

All recommended interventions must pass feasibility validation.

NFR-COR-004

The same scenario, state and rule version must produce the same output.

10.2 Performance

Initial MVP targets:

Operation	TargetScenario validation	p95 below 200 ms
Baseline impact calculation	p95 below 2 seconds
One intervention simulation	p95 below 1 second
Five-candidate comparison	p95 below 5 seconds
Evidence retrieval	p95 below 2 seconds
Full response without LLM	p95 below 8 seconds
Full response with LLM	p95 below 15 seconds
Historical scenario replay	p95 below 3 seconds

These are engineering targets to be tested later, not current performance claims.

10.3 Reliability
NFR-REL-001

A failed LLM call must not destroy deterministic simulation results.

NFR-REL-002

A failed candidate simulation must not invalidate successful candidates.

NFR-REL-003

The system must distinguish total failure from partial completion.

NFR-REL-004

Scenario execution must be idempotent when the same idempotency key is used.

10.4 Security
All SQL must be parameterized.
Secrets must remain outside source control.
Database permissions must follow least privilege.
Audit records must not be mutable through the normal application role.
Prompt content must not override calculation authority.
Sensitive configuration must not appear in logs or API responses.
10.5 Explainability

Every recommendation must expose:

Objective
Constraints
Candidate alternatives
Candidate metrics
Selection basis
Evidence references
Calculation version
Remaining risk
10.6 Usability

The judge-facing workflow should:

Communicate the problem within 10 seconds.
Create a seeded scenario within three interactions.
Display the do-nothing impact without requiring chat.
Compare interventions on one screen.
Open evidence within one additional interaction.
Avoid requiring knowledge of SQL.
10.7 Accessibility

Target:

Keyboard-accessible controls
Visible focus states
Non-color-only status indicators
Minimum WCAG AA contrast where practical
Labels for form controls
Text alternatives for charts
Responsive behavior at common laptop widths
10.8 Reproducibility

A clean environment must be able to:

Configure Db2.
Run migrations.
Seed the dataset.
Start the application.
Execute the golden scenario.
Reproduce the documented result.

No undocumented data correction is permitted.

Deliverable
docs/product/non-functional-requirements.md

11. Phase 1I: Data and evidence requirements
Goal

Define what information Phase 2 and Phase 3 must model and generate.

11.1 Required operational data
Supplier data
Supplier ID
Supplier name
Status
Region
Reliability information, if used
Approved components
Normal lead time
Capacity
Effective dates
Component data
Component ID
Description
Unit of measure
Criticality
Safety stock
Substitution group
Unit cost
Product and BOM data
Product ID
Component ID
Required quantity
Scrap or yield factor, if used
Effective date
Mandatory or optional status
Inventory data
Warehouse
Component
On-hand quantity
Reserved quantity
Available quantity
Safety-stock requirement
Snapshot time
Purchase orders
Purchase-order ID
Supplier
Component
Quantity
Expected arrival
Status
Expedite eligibility
Unit cost
Production orders
Production-order ID
Product
Quantity
Facility
Planned start
Planned completion
Priority
Capacity requirement
Customer orders
Customer-order ID
Product
Quantity
Promised date
Revenue
SLA class
Priority
Assigned production order
Intervention information
Alternate supplier
Transfer lead time
Transfer cost
Expedite cost
Supplier premium
Production rescheduling limits
11.2 Required evidence documents
Supplier disruption notices
Historical incident reports
Approved substitution procedures
Inventory-transfer procedure
Shipment-expedition procedure
Customer SLA policy
Recovery approval policy
11.3 Data quality requirements

The system must detect:

Missing foreign-key relationships
Negative quantities
Invalid date ordering
Duplicate active records
Expired substitutions
Unknown units
Conflicting inventory snapshots
Missing customer due date
Unsupported currencies
Unqualified alternate supplier
11.4 Evidence hierarchy

Use:

Level 1: Operational fact

Structured Db2 record.

Examples:

Inventory quantity
Purchase-order arrival date
Production schedule
Customer due date
Level 2: Deterministic derived value

Calculated from structured facts.

Examples:

Shortage date
Delay days
Revenue at risk
SLA status
Level 3: Controlled reference evidence

Retrieved procedure or historical incident.

Examples:

Transfer procedure
Alternate-supplier policy
Similar historical outage
Level 4: Generated explanation

LLM-generated narrative constrained by Levels 1–3.

Level 4 must never override Levels 1–2.

Deliverable
docs/product/data-and-evidence-requirements.md

Phase 2 dependency

Phase 2 must translate these requirements into:

Entities
Relationships
Causal paths
Temporal semantics
Business rules
Units and constraints
12. Phase 1J: AI authority and control specification
Goal

Define precisely what AI controls and what it cannot control.

AI component 1: Scenario Planner
Allowed
Extract supplier reference
Extract duration
Extract objective
Extract cost ceiling
Ask for missing required information
Return typed structured output
Forbidden
Invent supplier IDs
Invent budget
Calculate business impact
Create database records without validation
Select an intervention independently
AI component 2: Evidence selector
Allowed
Formulate retrieval query
Rank contextual relevance
Select relevant procedures or incidents
Forbidden
Treat retrieved text as operational truth
Bypass access filters
Use expired documents without warning
Convert a historical incident into a current-state fact
AI component 3: Decision narrator
Allowed
Explain verified calculations
Summarize comparisons
Explain trade-offs
Format an executive summary
Forbidden
Introduce a new number
Change a candidate score
Mark an infeasible intervention feasible
Hide warnings
Claim certainty not present in the structured output
AI failure policy

When AI is unavailable:

Capability	BehaviorNatural-language parsing	Use structured form
Evidence-query generation	Use predefined structured query
Recommendation narration	Use deterministic template
Simulation	Continue normally
Optimization	Continue normally
Audit	Record AI unavailability
Numerical claim contract

For every number produced in narrative text:

Claim
→ Structured field
→ Simulation run
→ Calculation rule
→ Source evidence


If the chain cannot be completed, the number must not be displayed.

Deliverable
docs/product/ai-authority-contract.md

Exit gate

Every planned AI capability is classified as:

ALLOWED
VALIDATED
FORBIDDEN
FALLBACK_AVAILABLE

13. Phase 1K: MVP and scope control
Goal

Protect the winning vertical slice from unnecessary expansion.

13.1 MVP, Priority 0

The minimum valid product must:

Accept a structured supplier outage.
Validate the supplier and duration.
Load a specified operational state from Db2.
Calculate do-nothing impact.
Evaluate inventory transfer.
Evaluate shipment expedition.
Evaluate alternate supplier.
Evaluate production rescheduling.
Compare at least five candidates including do nothing.
Select the best feasible candidate.
Display source evidence.
Preserve an audit record.
Produce a deterministic summary.
Run from documented setup instructions.

If any Priority 0 feature is absent, the core product is incomplete.

13.2 Winning core, Priority 1
Natural-language scenario creation
Db2 vector retrieval
Historical incident retrieval
Evidence drawer
Decision replay
Numerical claim verifier
Hybrid intervention
Baseline-versus-recommendation visualization
Benchmark comparison
13.3 Differentiators, Priority 2
Pareto frontier
Sensitivity analysis
Historical as-of state
Scenario duplication
Timeline replay
Confidence classification based on data completeness
Downloadable decision report
13.4 Deferred, Priority 3

Do not implement until Priority 0 and Priority 1 are stable:

Demand-spike scenarios
Warehouse closure
Production-line outage
Multi-event disruption
Monte Carlo simulation
Geographic route maps
Live ERP connectors
Autonomous agents
Multiple LLM providers
Automatic purchase-order execution
Real external supplier feeds
Scope-change process

A new feature enters the MVP only if:

It directly improves a judging category.
It does not delay a Priority 0 feature.
It has testable acceptance criteria.
Its data requirements are known.
Its failure behavior is known.
The decision is recorded in the decision log.
Deliverable
docs/product/scope-and-priority-register.md

14. Phase 1L: Judging-rubric alignment
Goal

Design visible proof for every judging criterion.

The official rubric weights IBM Db2 integration at 30%, innovation and impact at 25%, architecture and AI integration at 20%, reproducibility at 15%, and documentation and presentation at 10%.

14.1 IBM Db2 integration and depth: 30 points
Planned proof
Operational supply-chain records in Db2
Historical state in Db2
Scenario definitions in Db2
Simulation results in Db2
Decision audit in Db2
Evidence documents and embeddings in Db2
Structured and vector retrieval
Constraints, indexing and database roles
Query plans and measured performance
Demo moment

Open an evidence panel showing:

Scenario run
Impact calculation
Source rows
Historical incident
Audit record
Failure condition

Db2 acts only as a storage location for chatbot documents.

14.2 Innovation and real-world impact: 25 points
Planned proof
Counterfactual comparison, not only retrieval
Deterministic operational cascade
Feasibility-aware recommendations
Decision replay
Revenue and SLA trade-off
Evidence-backed recommendation
Impact metrics
SLA breaches avoided
Delay days reduced
Revenue at risk reduced
Recovery cost
Decision-analysis time
Failure condition

The product is presented as a generic RAG chatbot.

14.3 Technical architecture and AI integration: 20 points
Planned proof
Typed scenario planner
Deterministic impact engine
Isolated simulation engine
Constraint validator
Optimization layer
Hybrid evidence retrieval
Numerical claim verifier
Graceful non-LLM fallback
Failure condition

The architecture is five LLM prompts with no controlled calculation layer.

14.4 Reproducibility and code quality: 15 points
Planned proof
One-command or short documented setup
Dependency locks
Database migrations
Seed generator
Golden scenario
Automated tests
Benchmark runner
CI
Security scanning
Clear code boundaries
Failure condition

The demo works only on the creator’s machine.

14.5 Documentation and presentation: 10 points
Planned proof
Concise README
Architecture diagram
Db2-depth document
Benchmark report
Threat model
Screenshots
Three-minute video
Clear limitations
Reproduction steps
Failure condition

Strong code is hidden behind unclear documentation or a chat-only interface.

Rubric traceability matrix

Create fields:

criterion
weight
requirement_ids
feature
implementation_artifact
test_ids
metric
documentation_artifact
demo_timestamp
status

Deliverable
docs/product/rubric-evidence-matrix.csv

Exit gate

Every criterion must have:

At least one implementation artifact
At least one test
At least one metric
At least one documentation artifact
At least one demo moment
15. Phase 1M: Success metrics and evaluation contract
Goal

Define metrics before implementation so later benchmarks cannot be manipulated around observed results.

15.1 Product-correctness metrics
Impact precision
Impact Precision=correctly predicted affected entitiesall predicted affected entities\text{Impact Precision} = \frac{\text{correctly predicted affected entities}} {\text{all predicted affected entities}}

Target:

≥ 95%

Impact recall
Impact Recall=correctly predicted affected entitiesall actually affected entities\text{Impact Recall} = \frac{\text{correctly predicted affected entities}} {\text{all actually affected entities}}

Target:

≥ 95%


For the golden deterministic scenario, both should reach 100%.

15.2 Numerical fidelity
Numerical Fidelity=displayed numerical claims matching structured outputsall displayed numerical claims\text{Numerical Fidelity} = \frac{\text{displayed numerical claims matching structured outputs}} {\text{all displayed numerical claims}}

Target:

100%

15.3 Intervention feasibility
Feasibility Accuracy=correct candidate feasibility classificationsall candidate classifications\text{Feasibility Accuracy} = \frac{\text{correct candidate feasibility classifications}} {\text{all candidate classifications}}

Target:

100% for golden scenario
≥ 98% for benchmark suite

15.4 Recommendation agreement
Optimal Plan Agreement=scenarios where selected plan matches benchmark optimumevaluated benchmark scenarios\text{Optimal Plan Agreement} = \frac{\text{scenarios where selected plan matches benchmark optimum}} {\text{evaluated benchmark scenarios}}

Target:

≥ 90%


If multiple plans are tied or Pareto-efficient, the benchmark must recognize all valid answers.

15.5 Evidence coverage
Evidence Coverage=verifiable claims linked to evidenceall verifiable claims\text{Evidence Coverage} = \frac{\text{verifiable claims linked to evidence}} {\text{all verifiable claims}}

Target:

100%

15.6 AI parsing metrics
Valid structured scenario rate: at least 95%
Invalid-input rejection: 100%
Unknown supplier rejection: 100%
Unsupported objective rejection: 100%
Invented identifier acceptance: 0%
15.7 Retrieval metrics

Targets for the frozen evidence corpus:

Recall@5: at least 0.85
Precision@5: at least 0.75
Mean Reciprocal Rank: at least 0.80
Structured-filter compliance: 100%
Unauthorized-document retrieval: 0%
15.8 Performance metrics

Report:

Median
p95
Maximum
Error rate
Dataset size
Hardware
Db2 version
Warm versus cold execution

No single latency number should be reported without test conditions.

15.9 Human-understanding metrics

For a small evaluation with at least five reviewers, measure:

Can identify affected orders in under 30 seconds
Can identify recommended intervention in under 15 seconds
Can locate supporting evidence in under 30 seconds
Can explain the main trade-off after one viewing
Confidence in understanding, rated 1–5

These are usability measurements, not claims about commercial validation.

Deliverable
docs/product/measurement-contract.md

16. Phase 1N: Acceptance-test specification
Goal

Define product-level tests before implementation.

AT-001: Valid supplier outage
Given
Supplier S-104 exists.
It supplies critical component C-042.
The user provides a 14-day outage.
When

The scenario is created.

Then
Scenario is accepted.
A unique ID is assigned.
Start date and duration are stored.
Objective and constraints are preserved.
Original input remains immutable.
AT-002: Unknown supplier
Given

Supplier S-999 does not exist.

When

The user creates a scenario.

Then
Scenario execution does not begin.
Error code identifies an unknown supplier.
No simulation record is created.
An audit event records validation failure.
AT-003: Do-nothing impact
Given

A frozen golden scenario.

When

The baseline is calculated.

Then

Results exactly match:

Expected affected components
Expected affected production orders
Expected customer orders
Expected delay
Expected SLA breaches
Expected revenue at risk

Exact values will be defined in Phases 2 and 3.

AT-004: Safety-stock violation
Given

A warehouse has surplus stock above zero but below the transferable threshold.

When

An inventory-transfer candidate is evaluated.

Then

The candidate is marked infeasible with:

SOURCE_SAFETY_STOCK_VIOLATION

AT-005: Budget violation
Given

An intervention costs more than the scenario budget.

Then

It is marked infeasible or excluded from selection, but its projected operational result remains available for comparison if calculated.

AT-006: Alternate supplier not approved

An unapproved supplier must never be recommended.

AT-007: LLM unavailable

The deterministic workflow continues and produces a templated report.

AT-008: Unsupported numerical claim

If the narrator emits a value not present in structured results:

Verification fails.
The value is removed or the narrative is regenerated.
The failure is audited.
AT-009: Scenario isolation

Two scenarios using the same baseline but different outages must not modify one another.

AT-010: Decision replay

Loading a completed scenario must reproduce the stored decision state and original evidence links.

AT-011: No feasible intervention

The system returns:

NO_FEASIBLE_INTERVENTION


It must not recommend the least-invalid option.

AT-012: Insufficient data

Missing information required for calculation returns:

INSUFFICIENT_DATA


It must not be treated as zero.

Deliverable
docs/product/product-acceptance-tests.md

Exit gate

At least one acceptance test exists for every Priority 0 requirement group.

17. Phase 1O: Risks, assumptions and unresolved questions
Goal

Prevent hidden assumptions from entering the domain model.

Product assumptions to record
A-001

One supplier may supply multiple components.

A-002

A component may have multiple approved suppliers.

A-003

Products may require multiple components.

A-004

A production order is constrained by required component availability.

A-005

Customer orders are associated with products and delivery commitments.

A-006

Revenue at risk is the value of projected SLA-breaching orders, not confirmed revenue loss.

A-007

Recovery cost and revenue at risk use one normalized currency in the MVP.

A-008

Transportation capacity is simplified to transfer lead time and cost.

A-009

The MVP uses synthetic data.

A-010

Interventions require human approval.

Critical product questions Phase 2 must resolve
Domain questions
DOM-001 What exact entities define the supply-chain state?
DOM-002 Can one component substitute for another?
DOM-003 How are BOM effective dates handled?
DOM-004 How is reserved inventory allocated?
DOM-005 What causes a production order to be delayed?
DOM-006 How is customer-order delivery derived?

Temporal questions
TIME-001 What timestamp defines scenario state?
TIME-002 How are late-arriving updates handled?
TIME-003 Are snapshots daily, hourly or event-based?
TIME-004 What happens when records overlap in validity?

Financial questions
FIN-001 What exactly counts as recovery cost?
FIN-002 How is revenue at risk calculated?
FIN-003 Do partial order delays expose full or partial revenue?
FIN-004 How are currency and unit conversions handled?

Optimization questions
OPT-001 How are objectives normalized?
OPT-002 Which constraints are hard?
OPT-003 Which preferences are soft?
OPT-004 How are ties handled?
OPT-005 Can mixed interventions be partially applied?

Product risks
ID	Risk	Impact	Phase 1 treatmentP1-R01	Too many features dilute the core	Critical	Lock Priority 0 and 1
P1-R02	Revenue-at-risk definition is misleading	High	Define exact rule
P1-R03	AI receives calculation authority	Critical	Enforce AI contract
P1-R04	Simulation looks like prediction	High	Use precise terminology
P1-R05	Requirements cannot be tested	High	Acceptance-test mapping
P1-R06	Db2 appears superficial	Critical	Rubric evidence matrix
P1-R07	Synthetic dataset appears unrealistic	High	Domain rules in Phase 2
P1-R08	Optimization recommends infeasible action	Critical	Hard feasibility gate
P1-R09	No feasible plan is hidden	High	Explicit no-plan state
P1-R10	Success metrics are decided after results	High	Freeze measurement contract
Deliverables
docs/product/product-risk-register.md
docs/product/product-assumption-register.md
docs/product/phase-2-question-register.md

18. Phase 1P: Requirements quality benchmark
Goal

Measure whether the specification is complete enough to enter domain design.

18.1 Requirement coverage
RC=user needs mapped to requirementstotal user needsRC = \frac{\text{user needs mapped to requirements}} {\text{total user needs}}

Target:

100%

18.2 Use-case coverage
UC=Priority 0 requirements mapped to use casestotal Priority 0 requirementsUC = \frac{\text{Priority 0 requirements mapped to use cases}} {\text{total Priority 0 requirements}}

Target:

100%

18.3 Acceptance-test coverage
ATC=Priority 0 requirements with acceptance teststotal Priority 0 requirementsATC = \frac{\text{Priority 0 requirements with acceptance tests}} {\text{total Priority 0 requirements}}

Target:

100%


Priority 1 target:

≥ 80%

18.4 Rubric traceability
RT=rubric categories with implementation, test, metric and demo evidence5RT = \frac{\text{rubric categories with implementation, test, metric and demo evidence}} {5}

Target:

100%

18.5 Requirement ambiguity rate

Review all mandatory requirements and count those containing undefined qualitative terms.

Examples:

Fast
Intelligent
User-friendly
Accurate
Scalable
Reliable
Secure
Real-time
Optimal
AR=ambiguous mandatory requirementsall mandatory requirementsAR = \frac{\text{ambiguous mandatory requirements}} {\text{all mandatory requirements}}

Target:

0%

18.6 Orphan requirement rate

An orphan requirement has no user need, use case or acceptance method.

Target:

0%

18.7 Scope stability

Count proposed features that have not been assigned a priority.

Target:

0

18.8 Specification review exercise

Conduct three paper walkthroughs.

Walkthrough A: Normal case
Known supplier
14-day outage
Multiple feasible interventions
One clear best plan
Walkthrough B: No feasible recovery
Severe outage
Insufficient inventory
No approved alternative
Budget too low
Walkthrough C: Incomplete data
Missing inventory snapshot
Conflicting supplier capacity
Incomplete customer due date

For each walkthrough, verify that the specification determines:

Accepted input
Required calculation
Expected state
User-visible message
Audit behavior
Test behavior
Phase 1 scorecard
Category	WeightProduct clarity	10
User and stakeholder definition	10
Decision specification	15
Functional requirement completeness	15
Non-functional requirements	10
AI authority controls	10
Scope discipline	10
Rubric alignment	10
Measurement contract	5
Acceptance-test coverage	5
Total	100
Passing threshold
95–100: Pass
90–94: Conditional pass
Below 90: Fail

Automatic failures

Phase 1 fails regardless of score if:

The primary user is undefined.
The decision output is undefined.
Revenue at risk remains undefined.
The LLM is allowed to generate business calculations.
MVP scope is not locked.
A Priority 0 requirement lacks a verification approach.
Db2 depth has no planned proof.
“No feasible intervention” is not handled.
Insufficient data is treated as zero.
Success metrics are postponed until after implementation.
19. Phase 1Q: Phase 2 handoff
Goal

Provide Phase 2 with exact inputs for domain and causal modelling.

Phase 2 must receive
Product inputs
Locked product identity
Primary persona
Stakeholder priorities
Core decision
User journey
Use-case catalogue
Requirement inputs
Functional requirements
Non-functional requirements
Data requirements
Evidence requirements
AI authority contract
Acceptance tests
Scope inputs
Priority 0 features
Priority 1 features
Deferred features
Scope-change rules
Modelling questions
Entity questions
Temporal questions
Financial questions
Constraint questions
Optimization questions
Evaluation inputs
Measurement contract
Rubric evidence matrix
Acceptance-test identifiers
Phase 1 quality report
Phase 2 mandatory results

Phase 2 must convert this product specification into:

Entity model
Relationship model
Causal graph
Temporal model
State-transition model
Business-rule catalogue
Formula catalogue
Units and currency rules
Constraint catalogue
A manually solved golden scenario
20. Required Phase 1 repository structure
docs/product/
├── phase-0-handoff-review.md
├── product-identity.md
├── stakeholder-map.md
├── primary-persona.md
├── user-needs.md
├── decision-specification.md
├── end-to-end-user-journey.md
├── use-case-catalogue.md
├── functional-requirements.md
├── non-functional-requirements.md
├── data-and-evidence-requirements.md
├── ai-authority-contract.md
├── scope-and-priority-register.md
├── rubric-evidence-matrix.csv
├── measurement-contract.md
├── product-acceptance-tests.md
├── product-risk-register.md
├── product-assumption-register.md
├── phase-2-question-register.md
├── requirements-traceability-matrix.csv
└── phase-1-completion-report.md

21. Requirements traceability matrix

Create:

docs/product/requirements-traceability-matrix.csv


Recommended columns:

requirement_id
requirement_text
priority
stakeholder
user_need_id
use_case_id
journey_stage
data_requirement
acceptance_test_id
rubric_category
planned_phase
status
notes


Example:

FR-IMP-009,
Identify affected customer orders,
P0,
Supply-chain operations manager,
UN-003,
UC-002,
Do-nothing impact,
Customer orders and production mapping,
AT-003,
Innovation and Impact,
Phase 5,
Approved,

22. Phase 1 execution order

Follow this exact order.

Work Block 1: Validate foundation
1A. Verify Phase 0 artifacts
1A. Confirm locked technical decisions
1A. Record deferred foundation issues

Work Block 2: Lock product identity
1B. Finalize product descriptions
1B. Finalize product promise
1B. Finalize terminology constraints

Work Block 3: Define users and decision
1C. Define primary persona
1C. Define stakeholder map
1C. Define needs and conflicts
1D. Define inputs, outputs and decision boundary

Work Block 4: Define behavior
1E. Map complete user journey
1F. Write formal use cases
1F. Write alternate and failure flows

Work Block 5: Define requirements
1G. Write functional requirements
1H. Write non-functional requirements
1I. Write data and evidence requirements
1J. Lock AI authority

Work Block 6: Control scope
1K. Classify P0, P1, P2 and P3 features
1K. Record excluded functionality
1K. Define scope-change process

Work Block 7: Design evaluation
1L. Build rubric evidence matrix
1M. Freeze metrics and formulas
1N. Write acceptance tests

Work Block 8: Review and handoff
1O. Update risks and assumptions
1P. Calculate quality metrics
1P. Run three paper walkthroughs
1P. Resolve specification defects
1Q. Write Phase 1 completion report
1Q. Freeze Phase 2 inputs

23. Phase 1 final gate
Product definition
 Product identity is consistent.
 Primary user is defined.
 Secondary stakeholders are defined.
 Core problem is explicit.
 Core decision is explicit.
 Product inputs are defined.
 Product outputs are defined.
 Product limitations are defined.
User behavior
 Complete journey is mapped.
 Normal flow is documented.
 Alternate flows are documented.
 Failure flows are documented.
 No-feasible-plan behavior is documented.
 Insufficient-data behavior is documented.
 LLM-unavailable behavior is documented.
Requirements
 Functional requirements are atomic.
 Functional requirements have IDs.
 Non-functional targets are measurable.
 Data requirements are documented.
 Evidence requirements are documented.
 AI authority is bounded.
 Audit requirements are documented.
Scope
 Priority 0 is locked.
 Priority 1 is locked.
 Differentiators are separated.
 Deferred features are recorded.
 Scope-change process exists.
Judging
 All five judging categories are mapped.
 Db2-depth proof is defined.
 Innovation proof is defined.
 Architecture proof is defined.
 Reproducibility proof is defined.
 Presentation proof is defined.
Evaluation
 Correctness metrics are frozen.
 Retrieval metrics are frozen.
 AI metrics are frozen.
 Performance metrics are frozen.
 Usability metrics are frozen.
 Acceptance tests cover every Priority 0 group.
Handoff
 Phase 2 questions are documented.
 Requirements traceability is complete.
 No orphan Priority 0 requirement remains.
 Phase 1 score is at least 95.
 No automatic-failure condition remains.
 Phase 1 completion report is written.
Phase 1 Definition of Done

Phase 1 is complete only when this statement is true:

ChronosDB has a precise user, decision, workflow, scope, requirement set, evidence contract, AI authority boundary, judging strategy, measurement contract and acceptance-test suite. Every Priority 0 capability is traceable from user need to requirement to future test, and Phase 2 can construct the domain and causal model without inventing product behavior.

Locked output of Phase 1

After this phase, we should no longer debate:

What ChronosDB is
Who it serves
Which problem it solves
What the MVP contains
What the LLM may control
What the output means
How success will be measured

Phase 2 will begin with:

Domain, Temporal and Causal Model

Its first task will be to convert the Phase 1 requirements into the exact supply-chain entities, relationships, causal rules, time semantics, formulas and manually verified golden scenario.