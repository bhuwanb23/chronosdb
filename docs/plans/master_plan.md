Absolutely clear. The idea is now locked as ChronosDB: Auditable Counterfactual Intelligence for Supply-Chain Disruptions. We will treat the plan below as the project’s master execution framework, then take one phase at a time, investigate it deeply, produce its artifacts, run its gate, and only then move forward.

ChronosDB Master Build Plan
Project mission

Build an IBM Db2-native decision-intelligence system that can:

Reconstruct the operational state at any point in time.
Detect the cascading impact of a supply-chain disruption.
Simulate multiple recovery interventions.
Select the best feasible intervention under business constraints.
Explain every result using traceable Db2 evidence.
Replay and audit the full decision process.
Locked product statement

ChronosDB turns enterprise supply-chain data into an auditable counterfactual decision system that reconstructs the past, simulates possible futures, compares interventions, and proves every recommendation using IBM Db2 evidence.

Locked demonstration scenario

An electronics manufacturer depends on several suppliers, warehouses and production facilities.

A critical supplier becomes unavailable for 14 days. ChronosDB must calculate:

Affected components
Affected production orders
Affected customer orders
Inventory shortfalls
SLA violations
Delay duration
Revenue at risk
Alternative interventions
Intervention cost
Revenue protected
Best feasible recovery plan
Execution principles

These rules apply to every phase.

Rule 1: Db2 is the execution backbone

IBM Db2 must not be used merely as a place to store documents. It must support:

Operational records
Historical state
Vector embeddings
Semantic evidence retrieval
Scenario definitions
Simulation outcomes
Decision audit history
Agent and model traces
Benchmark results
Rule 2: LLMs do not calculate business results

The LLM may:

Interpret a user request
Convert it into a validated scenario
Retrieve explanatory evidence
Explain verified results

The LLM may not independently calculate:

Revenue at risk
Inventory depletion
Delay duration
SLA breaches
Intervention cost
Optimal recovery plan

Those outputs must come from deterministic SQL or application logic.

Rule 3: Every important claim requires evidence

Every displayed metric must be connected to:

Scenario run ID
Db2 source records
Calculation version
Timestamp
Units
Evidence query or rule
Verification status
Rule 4: One strong vertical slice before expansion

We will first make supplier outage → impact cascade → intervention comparison → evidence replay work end to end.

Demand spikes, warehouse failures and production-capacity failures come later.

Rule 5: No phase passes through screenshots alone

A phase passes only when its required:

Code
Tests
Documentation
Measured results
Reproduction instructions

are complete.

Phase map
| Phase | Name | Primary outcome |
| --- | --- | --- |
| 0 | Project Control and Submission Safety | Establish constraints, repository and working baseline |
| 1 | Product and Judging Specification | Convert the idea into measurable requirements |
| 2 | Domain and Causal Model | Define the supply-chain system and disruption mechanics |
| 3 | Dataset Engineering | Produce a coherent, validated demonstration dataset |
| 4 | Db2 Data Architecture | Implement Db2 schema, constraints, roles and indexes |
| 5 | Deterministic Impact Engine | Calculate cascading disruption impact |
| 6 | Counterfactual Simulation Engine | Run alternative future scenarios |
| 7 | Intervention Optimization | Rank feasible recovery actions |
| 8 | Evidence and Retrieval Layer | Add Db2-native semantic and structured evidence |
| 9 | Controlled AI Orchestration | Add typed planning and verified narration |
| 10 | Trust, Security and Auditability | Protect the system and preserve decision history |
| 11 | Backend and API Integration | Expose the full workflow through stable APIs |
| 12 | Judge-Facing User Experience | Build the visual operations war room |
| 13 | Benchmark and Evaluation System | Measure correctness, retrieval, speed and safety |
| 14 | Testing and Reliability | Validate all normal and failure paths |
| 15 | Packaging and Reproducibility | Make the project runnable from a clean environment |
| 16 | Documentation and Architecture Package | Produce evaluator-ready technical documentation |
| 17 | Demo, Storytelling and Visual Assets | Build the three-minute judging experience |
| 18 | Submission Compliance | Complete every official submission requirement |
| 19 | Final Red-Team and Release Gate | Run the final independent acceptance review |
| 20 | Post-Submission and IBM Contribution Readiness | Prepare a clean reusable upstream use case |
Phase 0: Project Control and Submission Safety
Objective

Create a controlled project environment before implementation begins.

Workstreams
0.1 Submission-status verification

Because the public event information previously showed conflicting deadline details, establish:

Whether registration is complete
Whether an initial PR already exists
Whether the Google Form has been submitted
Whether post-deadline PR commits are accepted
Whether the project must remain an individual submission
Whether a specific framework is mandatory
Whether LinkedIn posting is mandatory
0.2 Source-of-truth register

Create:

docs/project-control/
├── official-requirements.md
├── judging-rubric.md
├── submission-checklist.md
├── assumptions-register.md
├── risk-register.md
└── decision-log.md

0.3 Repository initialization

Set up:

Submission branch
Project directory
.env.example
.gitignore
Python environment
Node environment if required
Formatter
Linter
Test runner
Pre-commit checks
Basic CI workflow
0.4 Version baseline

Record exact versions for:

IBM Db2
Python
ibm_db
LangChain or LangGraph
Embedding model
LLM provider
FastAPI
Frontend framework
Docker or local Db2 environment
Deliverables
Compliant repository skeleton
Requirements register
Risk register
Decision log
Environment version matrix
Initial CI check
Submission safety report
Exit gate

Phase 0 passes only when:

The repository builds in a clean environment.
No secret is committed.
Official requirements are documented.
The project path and branch naming are compliant.
Submission risks have an owner and mitigation.
One minimal application-to-Db2 connection test passes.
Phase 1: Product and Judging Specification
Objective

Translate the idea into a precise product specification aligned with the judging rubric.

Workstreams
1.1 User definition

The primary user will be an operations or supply-chain manager responsible for:

Supplier disruption response
Inventory allocation
Production continuity
Customer-service commitments
Recovery-cost control
1.2 Core user journey

The complete journey must be defined:

Select or describe a disruption.
Validate the disruption parameters.
Create an immutable scenario.
Reconstruct the relevant operational state.
Determine the baseline impact.
Generate feasible intervention candidates.
Simulate each intervention.
Rank outcomes against constraints.
Explain the recommendation.
Inspect Db2 evidence.
Replay and audit the decision.
1.3 Functional requirements

Assign identifiers:

FR-001 Create supplier-outage scenario
FR-002 Validate supplier and disruption duration
FR-003 Reconstruct historical operational state
FR-004 Determine affected components
FR-005 Determine affected production orders
FR-006 Determine affected customer orders
FR-007 Calculate SLA impact
FR-008 Calculate revenue at risk
FR-009 Generate intervention candidates
FR-010 Reject infeasible interventions
FR-011 Rank feasible interventions
FR-012 Retrieve relevant operational evidence
FR-013 Generate verified explanation
FR-014 Store immutable audit record
FR-015 Replay a previous decision

1.4 Non-functional requirements

Define measurable targets for:

Correctness
Numerical fidelity
Retrieval quality
Response latency
Reproducibility
Security
Availability
Auditability
Accessibility
UI responsiveness
1.5 Rubric evidence matrix

For every judging category, document:

Feature that addresses it
Artifact that proves it
Demo moment that shows it
Metric that measures it
Failure conditions
Deliverables
Product requirements document
User journey
Acceptance criteria
Rubric-to-evidence matrix
Defined MVP boundary
Deferred-feature register
Exit gate
Every feature maps to a user requirement.
Every judging criterion maps to visible evidence.
MVP and optional features are separately identified.
No requirement depends on an undefined “intelligent agent.”
Numerical claims have planned calculation ownership.
Phase 2: Domain and Causal Model
Objective

Define exactly how supply-chain entities, constraints and disruptions interact.

Workstreams
2.1 Entity model

Define:

Supplier
Component
Product
Bill of materials
Warehouse
Facility
Inventory lot
Purchase order
Production order
Customer order
Customer SLA
Shipment
Disruption
Intervention
Simulation run
Decision record
2.2 Dependency model

Establish deterministic relationships:

Supplier
→ Component
→ Bill of materials
→ Product
→ Production order
→ Customer order
→ SLA and revenue

2.3 Time semantics

Define:

Event time
Ingestion time
Effective time
Expected arrival time
Production start and end
Customer due date
Scenario as-of time
Simulation horizon
2.4 Business rules

Examples:

Shortage begins when required quantity exceeds usable inventory before replenishment.
A production order is delayed if any mandatory BOM component is unavailable.
A customer order breaches SLA when projected completion exceeds its committed date.
Revenue is “at risk,” not necessarily “lost,” when an order is projected to breach its SLA.
Alternate supplier substitution is allowed only for approved components.
Warehouse transfer is feasible only when source safety stock remains above its minimum.
2.5 Uncertainty model

Separate:

Known facts
Derived deterministic values
Configurable assumptions
Forecast values
LLM-generated explanations
Deliverables
Domain dictionary
Entity relationship model
Causal dependency map
Business-rule catalogue
Time-semantics specification
Uncertainty classification
Worked scenario by hand
Exit gate
A complete supplier-outage scenario can be calculated manually.
All units are explicit.
No circular dependency is unresolved.
Every simulation parameter has a valid range.
All output metrics have exact definitions.
Phase 3: Dataset Engineering
Objective

Build a realistic, internally consistent dataset that demonstrates the complete problem.

Dataset target

A practical initial dataset could contain:

15–25 suppliers
60–100 components
10–20 finished products
3 warehouses
2 production facilities
250–500 purchase orders
150–300 production orders
500–1,000 customer orders
50–100 disruption reports
20–50 operational procedures
At least 90 days of state history

The precise final size should be large enough to appear realistic but small enough to inspect and reproduce quickly.

Workstreams
3.1 Data generation specification

Specify:

Primary keys
Dates
Quantities
Costs
Currencies
Lead times
Capacity values
SLA levels
Distribution assumptions
Referential relationships
3.2 Golden scenario creation

Create one carefully engineered supplier-outage scenario with known results.

3.3 Benchmark scenario generation

Create at least:

10 supplier outages
10 shipment delays
10 demand spikes
5 inventory-loss events
5 production-capacity reductions
10 multi-event scenarios
3.4 Ground-truth outcomes

For every benchmark case, preserve:

Expected affected entities
Expected shortage
Expected delay
Expected SLA breaches
Expected feasible interventions
Expected optimal intervention
3.5 Data validation

Check:

Foreign-key integrity
Non-negative quantities
Valid date ordering
Unique identifiers
Consistent currencies
Feasible production relationships
No impossible BOM structures
No orders referencing unavailable products
Deliverables
Seed dataset
Data generator
Data dictionary
Golden scenario
Benchmark scenarios
Expected outcomes
Validation report
Exit gate
Clean database seeding succeeds repeatedly.
Golden scenario produces manually verified results.
No referential-integrity errors remain.
Benchmark outcomes are version-controlled.
Synthetic nature and generation assumptions are disclosed.
Phase 4: Db2 Data Architecture
Objective

Implement Db2 as the operational, temporal, vector and audit backbone.

Workstreams
4.1 Operational schema

Implement normalized tables for:

Supply
Inventory
Production
Orders
Disruptions
Scenarios
Simulations
Decisions
4.2 Constraints

Add:

Primary keys
Foreign keys
Unique constraints
Check constraints
Non-negative quantity checks
Valid status checks
Date consistency checks
4.3 Historical model

Implement a consistent history approach using:

Effective-from and effective-to fields
State snapshot tables
Event ledger
Scenario AS_OF_TIMESTAMP
4.4 Vector schema

Store embeddings for:

Disruption reports
Supplier notices
Operating procedures
Historical incident summaries

Retain:

Source ID
Document version
Chunk identifier
Embedding model
Embedding dimension
Ingestion timestamp
4.5 Audit schema

Create separate tables for:

Scenario requests
Simulation runs
Candidate actions
Final decisions
Evidence associations
Model calls
Verification status
Errors
4.6 Roles and permissions

At minimum:

Read-only application role
Simulation writer role
Audit writer role
Administrative migration role
Deliverables
Schema migrations
Index strategy
Role and permission scripts
Db2 architecture document
Seed scripts
Schema verification tests
Query-plan samples
Exit gate
Database creates from zero without manual repair.
All constraints pass.
Unauthorized writes fail.
Historical reconstruction query works.
Vector insertion and retrieval work.
Scenario and audit records survive application restart.
Phase 5: Deterministic Impact Engine
Objective

Calculate the complete impact cascade without relying on an LLM.

Required calculation path
Disrupted supplier
→ Delayed or unavailable components
→ Projected inventory shortage
→ Affected production orders
→ Affected customer orders
→ SLA breaches
→ Revenue at risk

Workstreams
5.1 Inventory projection

Calculate:

Opening available stock
Reserved stock
Expected consumption
Confirmed replenishment
Delayed replenishment
Safety stock
Shortage date
Shortage quantity
5.2 BOM traversal

Determine all finished products affected by disrupted components.

5.3 Production impact

Calculate:

Earliest feasible start
Component-constrained start
Capacity-constrained start
Projected completion
Delay days
5.4 Customer impact

Calculate:

Affected customer orders
Projected delivery
SLA status
Priority
Revenue at risk
5.5 Explainable calculation trace

For every outcome, preserve intermediate values and rule IDs.

Deliverables
Impact engine
Rule catalogue
Calculation trace format
Unit tests
Golden scenario results
Performance measurements
Exit gate
Golden scenario exactly matches expected results.
Numerical output is reproducible.
Calculation traces explain each result.
No LLM call is needed.
Difference between revenue at risk and confirmed loss is maintained.
Edge cases pass.
Phase 6: Counterfactual Simulation Engine
Objective

Run multiple hypothetical futures from the same initial state.

Required scenarios
Do nothing
Transfer warehouse inventory
Expedite an existing order
Use an approved alternate supplier
Reschedule production
Combine multiple interventions
Workstreams
6.1 Immutable baseline

A simulation must never mutate live baseline data.

6.2 Scenario overlay

Apply changes as an isolated overlay:

Added supply
Changed lead time
Changed component allocation
Changed production priority
Changed transfer quantity
6.3 Simulation ledger

Record:

Initial state reference
Intervention definition
Rule version
Outputs
Runtime
Warnings
Errors
6.4 Comparative engine

Calculate differences between:

Baseline
Do-nothing scenario
Each intervention scenario
Deliverables
Scenario data model
Simulation service
Scenario isolation tests
Before-and-after comparison
Persistence layer
Repeatability report
Exit gate
Re-running a scenario produces identical results.
Parallel scenarios do not contaminate one another.
Base operational records remain unchanged.
Every outcome links to the exact scenario input.
At least five interventions can be compared.
Phase 7: Intervention Optimization
Objective

Select the best feasible intervention under explicit constraints.

Candidate objectives
Minimize SLA breaches
Minimize revenue at risk
Minimize recovery cost
Minimize delay
Maximize service level
Balance cost and customer impact
Constraints

Examples:

Maximum additional cost
Minimum safety stock
Maximum supplier capacity
Approved supplier relationships
Warehouse transfer limits
Production capacity
Maximum acceptable delay
Workstreams
7.1 Feasibility screening

Reject impossible interventions before ranking.

7.2 Scoring

Use normalized business metrics rather than arbitrary LLM rankings.

7.3 Pareto comparison

Show when no single plan is best on all dimensions.

7.4 Sensitivity analysis

Test whether the selected plan changes when:

Cost weight changes
SLA weight changes
Supplier lead time changes
Disruption duration changes
Deliverables
Intervention generator
Constraint validator
Scoring model
Pareto frontier output
Sensitivity report
Optimization tests
Exit gate
All recommended plans are feasible.
Ranking is reproducible.
Weights are visible and configurable.
A user can understand why one candidate outranks another.
Benchmark optimal-plan agreement reaches the established target.
Phase 8: Evidence and Retrieval Layer
Objective

Retrieve relevant historical incidents and operational procedures using Db2.

Retrieval sources
Supplier disruption reports
Historical incident summaries
Recovery procedures
Component substitution rules
SLA policies
Warehouse-transfer procedures
Workstreams
8.1 Document ingestion

Implement:

Parsing
Chunking
Metadata
Embedding
Versioning
Duplicate detection
8.2 Structured retrieval

Filter by:

Supplier
Component
Region
Incident type
Effective date
Document status
User access
8.3 Vector retrieval

Retrieve semantically related incidents and procedures.

8.4 Hybrid ranking

Combine semantic score with structured relevance and recency.

8.5 Evaluation

Measure:

Recall@K
Precision@K
Mean Reciprocal Rank
Metadata-filter accuracy
Unsupported-source rate
Deliverables
Ingestion pipeline
Vector search implementation
Hybrid retrieval logic
Retrieval benchmark
Source viewer
Evidence-link schema
Exit gate
Retrieval uses Db2 vector functionality.
Expired or unauthorized documents are excluded.
Benchmark targets are met or limitations documented.
Retrieved evidence links back to the source.
Retrieval failure does not fabricate evidence.
Phase 9: Controlled AI Orchestration
Objective

Add natural-language interaction without allowing the model to control business truth.

Component 1: Scenario Planner

Convert:

“Supplier S-104 is down for two weeks. Keep recovery under ₹2 lakh.”

into a typed request.

Component 2: Evidence Selector

Select which verified simulation outputs and retrieved sources are relevant to the response.

Component 3: Decision Narrator

Explain trade-offs using only approved evidence.

Workstreams
9.1 Structured output

Use a strict schema for:

Event type
Entity identifiers
Duration
Optimization objective
Constraints
As-of time
9.2 Validation

Reject:

Unknown entity
Impossible duration
Negative cost
Unsupported objective
Missing required parameters
9.3 Claim verifier

Check every generated numerical claim against structured results.

9.4 Graceful fallback

If the model fails:

Preserve simulation results.
Show a deterministic summary.
Record the model failure.
Never hide the underlying evidence.
Deliverables
Planner prompt and schema
Scenario validator
Narrator prompt
Claim verifier
Prompt-injection tests
Model-failure fallback
Model-call audit records
Exit gate
The LLM cannot modify operational tables.
Invalid plans are blocked.
Every number in the narrative matches verified output.
Prompt-injected documents cannot override system rules.
The application remains usable when the LLM is unavailable.
Phase 10: Trust, Security and Auditability
Objective

Make the project credible as an enterprise decision system.

Threats to cover
SQL injection
Prompt injection
Unauthorized writes
Cross-user data leakage
Secret exposure
Audit alteration
Unsupported recommendations
Malformed scenario requests
Duplicate execution
Denial through extreme inputs
Workstreams
Least-privilege Db2 accounts
Parameterized queries
Read-only query boundaries
Input validation
Secret management
Append-oriented decision auditing
Hashing or checksums for critical records
Correlation IDs
Failure logging
Redaction rules
Deliverables
Threat model
Security architecture
Role matrix
Adversarial test suite
Audit-integrity test
Security limitations
Exit gate
Destructive prompts cannot produce writes.
SQL injection tests fail safely.
No credentials are committed.
Every decision is traceable.
Audit records cannot be modified by the normal application role.
Security failures are visible rather than silently ignored.
Phase 11: Backend and API Integration
Objective

Expose a clean, stable end-to-end workflow.

Suggested API surface
POST /scenarios
POST /scenarios/{id}/simulate
GET  /scenarios/{id}
GET  /scenarios/{id}/impact
GET  /scenarios/{id}/interventions
GET  /scenarios/{id}/evidence
GET  /scenarios/{id}/audit
POST /scenarios/{id}/explain
GET  /health
GET  /readiness

Workstreams
Request and response schemas
Error taxonomy
Transaction boundaries
Idempotency
Timeouts
Correlation IDs
OpenAPI documentation
Health and readiness checks
Structured logs
Deliverables
FastAPI service
OpenAPI specification
API tests
Error catalogue
Health checks
End-to-end trace
Exit gate
Complete scenario runs through API only.
Invalid input returns useful errors.
Repeated requests do not create inconsistent duplicates.
Service failures preserve audit history.
API documentation matches actual behavior.
Phase 12: Judge-Facing User Experience
Objective

Create a memorable operations war-room experience.

Required views
12.1 Executive impact view

Show:

Revenue at risk
SLA breaches
Production delays
Affected orders
Recommended intervention
Revenue protected
12.2 Dependency cascade

Show the path from supplier disruption to customer impact.

12.3 Intervention comparison

Compare:

Cost
Delay
SLA breaches
Revenue protected
Risk
Feasibility
12.4 Timeline and replay

Allow movement between operational states and decision stages.

12.5 Evidence drawer

Show:

Source records
Retrieved procedures
Calculation rules
Scenario ID
Audit ID
Claim verification status
12.6 Degraded states

Design:

Loading
No results
Invalid scenario
Db2 unavailable
LLM unavailable
Partial evidence
Simulation failure
Deliverables
Design system
Responsive interface
Judge demo mode
Evidence explorer
Accessibility review
Final screenshots
Exit gate
The main value is understandable within 10 seconds.
The demo does not require judges to read long text.
No important number is presented without evidence access.
Core workflow works at standard laptop resolution.
Demo mode is stable and uses deterministic seeded data.
Phase 13: Benchmark and Evaluation System
Objective

Compare ChronosDB against meaningful baselines.

Required baselines
Naive LLM
Standard RAG
Rule-only simulator
Full ChronosDB
Metrics
Correctness
Impact precision
Impact recall
SLA classification accuracy
Numerical fidelity
Intervention feasibility
Optimal-plan agreement
Retrieval
Recall@5
Precision@5
Mean Reciprocal Rank
Filter compliance
AI reliability
Scenario parse success
Invalid-input rejection
Unsupported claim rate
Citation coverage
Performance
Median latency
p95 latency
Maximum latency
Simulation runtime
Retrieval runtime
Security
Injection attempts blocked
Unauthorized writes blocked
Prompt-injection success rate
Secret-scan findings
Deliverables
Benchmark runner
Frozen benchmark dataset
Baseline implementations
Machine-readable results
Human-readable report
Charts for README and demo
Limitations statement
Exit gate
Another evaluator can reproduce the benchmark.
All claims in the README come from stored results.
Failed cases are disclosed.
Synthetic benchmarks are identified as synthetic.
ChronosDB demonstrates measurable improvement on its intended dimensions.
Phase 14: Testing and Reliability
Objective

Prove that the system works beyond the golden demo.

Test layers
Unit tests
SQL tests
Schema tests
Integration tests
End-to-end tests
Adversarial tests
Performance tests
Reproducibility tests
UI flow tests
Failure-recovery tests
Critical cases
Supplier does not exist
Duration is zero or negative
No affected orders
Complete inventory shortage
Alternate supplier unavailable
Budget too small
Equal-scoring interventions
Missing document embedding
Db2 reconnect
LLM timeout
Duplicate API request
Corrupted scenario input
Deliverables
Test inventory
Automated test suite
Coverage report
Known-failure register
Reliability report
Exit gate
All critical-path tests pass.
No unresolved severity-one defect remains.
Golden demo passes repeatedly.
Known limitations are documented.
Clean-state and restart tests pass.
Phase 15: Packaging and Reproducibility
Objective

Allow an evaluator to run the project with minimal effort.

Target commands
make setup
make seed
make test
make benchmark
make demo


Where feasible, consolidate demo startup into:

make demo

Workstreams
Environment configuration
Db2 startup procedure
Schema migration
Dataset seeding
Embedding preparation
Application startup
Health verification
Cleanup
Troubleshooting
Deliverables
Docker or documented Db2 setup
Makefile
.env.example
Dependency lock files
Clean-install test
Troubleshooting guide
Reproduction video or terminal recording
Exit gate
A clean machine can run the documented process.
No undisclosed manual database edits are required.
Missing optional AI credentials produce a clear fallback.
Setup instructions use copyable commands.
Seeded demo produces expected results.
Phase 16: Documentation and Architecture Package
Objective

Make the technical depth obvious without forcing judges to inspect every source file.

Required documents
README.md
architecture.md
db2-deep-dive.md
benchmark-results.md
threat-model.md
limitations.md
demo-script.md
data-dictionary.md
decision-log.md
README order
One-sentence hook
Demo visual
Problem
Solution
Why IBM Db2
Golden scenario
Architecture
Measured results
Setup
Test commands
Security
Limitations
Future work
Deliverables
Full documentation suite
Architecture diagrams
Schema diagram
Data-flow diagram
Decision-flow diagram
Benchmark results
Screenshot set
Exit gate
Setup steps have been tested verbatim.
All diagrams match implementation.
No unsupported performance claim remains.
Db2 usage is visible and specific.
Limitations are honest and clear.
Phase 17: Demo, Storytelling and Visual Assets
Objective

Deliver a polished three-minute proof, not a feature tour.

Locked story
A supplier disruption occurs.
ChronosDB identifies the cascade.
It calculates the do-nothing impact.
It compares feasible recovery plans.
It recommends the best plan.
It opens the evidence trail.
It replays the decision through time.
Required assets
2–3 minute demo video
Captions
Clean voice-over
Stable seeded scenario
Architecture graphic
Db2 depth graphic
Benchmark graphic
Six to eight strong screenshots
Backup recorded demo
Deliverables
Final script
Shot list
Final recording
Captions
Thumbnail
Screenshot package
Backup demo path
Exit gate
The value proposition is clear in the first 20 seconds.
Db2 appears as a core component, not a logo.
The project’s uniqueness is said and shown.
No live dependency can destroy the recorded demo.
All displayed numbers match benchmark or scenario results.
Phase 18: Submission Compliance
Objective

Complete all official delivery requirements without administrative failure.

Checklist categories
Repository
Correct folder
Complete source
Correct metadata
License
.env.example
No secrets
Documentation
Screenshots
Tests
Pull request
Correct branch
Correct base repository
Required PR template
Clear project summary
Working links
CI passing
External submission
PR URL submitted
Demo video accessible
Form completed
LinkedIn requirement completed if mandatory
Correct participant information
Final timestamps recorded
Deliverables
Compliance checklist
Final PR
Submission evidence
Link-validation report
Secret-scan report
Exit gate
Every mandatory item has evidence.
All public links work in a logged-out browser.
Video permissions are correct.
PR renders correctly.
No credential or private information is exposed.
Phase 19: Final Red-Team and Release Gate
Objective

Review the project as a skeptical judge and hostile user.

Review perspectives
Judge review
Is the problem important?
Is innovation visible?
Is Db2 usage deep?
Is the result measurable?
Can the project be reproduced?
Are claims believable?
Technical review
Can results be reproduced?
Can numerical values be traced?
Are failure states handled?
Are permissions meaningful?
Are tests genuine?
Adversarial review
Can instructions be injected?
Can SQL be manipulated?
Can audit history be altered?
Can extreme inputs crash the system?
Can the model invent a numerical claim?
Deliverables
Final defect list
Rubric scorecard
Go/no-go assessment
Release tag or commit
Checksums for final artifacts
Exit gate
No critical defect remains.
Judge-facing path passes three consecutive times.
Benchmark results correspond to the release commit.
Final documentation corresponds to the release.
Submission links refer to the final version.
Phase 20: Post-Submission and IBM Contribution Readiness
Objective

Prepare ChronosDB to become more than a one-time hackathon demo.

Workstreams
Clean reusable sample dataset
Generalized configuration
IBM Db2 connector abstraction
Contribution-quality documentation
Issue templates
Developer guide
Extension roadmap
Demonstration notebook
Removal of competition-specific shortcuts
Potential extensions
Demand-spike simulation
Warehouse closure
Production-line failure
Multi-supplier correlated disruption
Monte Carlo uncertainty
Human approval workflow
Real ERP ingestion
SAP or Oracle integration
Geospatial logistics visualization
Carbon-cost optimization
Exit gate
The core use case runs without competition-specific assumptions.
Architecture boundaries support additional disruption types.
Repository can be reviewed as a reusable Db2 example.
Technical debt introduced for the deadline is documented.
Cross-phase workstreams

These must remain active throughout the project.

A. Decision log

For every major choice, record:

Decision
Date
Reason
Alternatives
Consequences
Reversal condition
B. Risk register

Track at least:

| Risk | Impact | Primary mitigation |
| --- | --- | --- |
| Db2 environment instability | Critical | Validate connection and seed process first |
| Vector feature/version mismatch | High | Detect Db2 version and provide clear compatibility behavior |
| LLM API unavailable | Medium | Deterministic fallback summary |
| Scope explosion | Critical | Lock supplier-outage vertical slice |
| Weak benchmark | High | Freeze ground-truth scenarios early |
| Attractive but shallow UI | High | Complete deterministic core before polish |
| Submission failure | Critical | Treat compliance as its own phase |
| Unsupported claims | High | Generate metrics directly from benchmark artifacts |
C. Traceability matrix

Maintain the chain:

Judging criterion
→ Requirement
→ Feature
→ Implementation
→ Test
→ Benchmark
→ Documentation
→ Demo moment

D. Definition of done

A feature is complete only when it has:

Implementation
Automated test
Error handling
Audit behavior
Documentation
Demo representation where relevant
Priority tiers
Tier 0: Mandatory to have a valid project
Working Db2 integration
Official framework integration
Functional source code
Setup instructions
Architecture documentation
Screenshots
Demo video
PR and form compliance
Tier 1: Required for the winning core
Deterministic impact engine
Scenario isolation
Five intervention comparisons
Evidence links
Db2 vector retrieval
Numerical claim verification
War-room dashboard
Benchmark suite
Security tests
Tier 2: Strong differentiators
Historical replay
Pareto frontier
Sensitivity analysis
Decision audit explorer
Hybrid structured and vector retrieval
Model-outage fallback
Tier 3: Only if the winning core is complete
Monte Carlo simulation
Multi-event disruptions
Geographic visualization
Multiple LLM providers
Autonomous agent debate
Real-time external feeds
ERP integration
Recommended implementation order

The numbered phases define the governance sequence, but the practical build order should be:

Phase 0  Project control
Phase 1  Requirements
Phase 2  Domain model
Phase 3  Golden dataset
Phase 4  Db2 schema
Phase 5  Impact engine
Phase 6  Simulation engine
Phase 7  Optimization
Phase 11 Minimal APIs
Phase 8  Evidence retrieval
Phase 9  AI layer
Phase 10 Security and audit
Phase 12 UI
Phase 13 Benchmarking
Phase 14 Reliability
Phase 15 Packaging
Phase 16 Documentation
Phase 17 Demo
Phase 18 Submission
Phase 19 Release review
Phase 20 Post-submission preparation


Backend APIs are introduced early enough to connect the deterministic system, but they are finalized after the computational core is stable.

Milestone gates
Milestone M1: Foundation complete

Includes Phases 0–4.

Proof: A clean Db2 database can be created and seeded with a verified golden scenario.

Milestone M2: Decision engine complete

Includes Phases 5–7.

Proof: The system deterministically calculates impact and selects a feasible recovery plan.

Milestone M3: Trustworthy AI complete

Includes Phases 8–10.

Proof: Natural-language interaction and semantic evidence work without transferring numerical authority to the LLM.

Milestone M4: Product complete

Includes Phases 11–12.

Proof: A user can complete the entire workflow through the application.

Milestone M5: Evidence complete

Includes Phases 13–16.

Proof: Correctness, security, speed and reproducibility are measured and documented.

Milestone M6: Submission complete

Includes Phases 17–19.

Proof: A judge can understand, run, verify and evaluate the submitted release.

How we will work phase by phase

When you ask for a phase, we will not merely expand these bullets. For each phase, we will produce:

Purpose and boundaries
Questions that must be answered
Design decisions
Exact tasks and subtasks
Technical implementation
Schemas, APIs or algorithms
Test cases
Expected artifacts
Risks and mitigations
Acceptance criteria
Exit-gate checklist
Inputs required by the following phase

We will maintain the locked decisions from completed phases and avoid silently changing the architecture later.

Starting point

The first detailed execution unit is:

Phase 0: Project Control, Submission Safety and Repository Baseline

That phase must resolve submission eligibility and deadline risk immediately, then establish the repository, environment, decision register, requirements register and initial Db2 connectivity baseline.