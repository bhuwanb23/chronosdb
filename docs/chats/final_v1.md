End-to-end benchmark: ChronosDB AI
Executive verdict

The original“Enterprise Digital Twin AI” direction is visually attractive, but it is currently too broad and too close to generic agentic RAG. “Historian, Analyst, Predictor, Simulator, Optimizer” sounds sophisticated, yet without a concrete domain, deterministic simulation, real data, and measurable validation, judges may perceive it as five LLM prompts wrapped around Db2.

### The strongest repositioning is:

ChronosDB: Auditable Counterfactual Intelligence for Supply-Chain Disruptions

A Db2-native decision engine that reconstructs what happened, simulates what could happen, recommends an intervention, and proves every conclusion with temporal database evidence.

This is narrower, more credible, easier to demonstrate, and meaningfully different from the visible competition.

One critical timing issue: the official sources state that submissions closed on 10 November 2026 at 5:00 PM IST, while the current date is 11 November 2026. If your PR and Google Form were not already submitted, confirm immediately with the organizers whether updates or late submissions are permitted. The public Devpost page also displays inconsistent deadline information, so preserve screenshots and organizer messages.

## 1. What the visible competition tells us

### The publicly discoverable projects are much stronger than generic hackathon prototypes. The apparent competitive standard is not “make a chatbot.” It is:

A narrowly defined enterprise problem
Non-trivial Db2 functionality
Deterministic safeguards around the LLM
Measured results
Reproducible deployment
A focused, credible demo
Competitive project benchmark
| Visible project | What makes it strong | Threat to ChronosDB | Gap we can exploit |
| --- | --- | --- | --- |
| NEEDLE | Searches more than 26,000 OSV advisories using hybrid semantic and keyword retrieval, Db2 row permissions, temporal exposure history, exact version joins and deterministic verification. It reports zero leaks in its held-out access-control test. | Very high | It diagnoses current vulnerability exposure. It does not appear to perform counterfactual operational simulation or intervention optimization. |
| MetricGuard | Uses AI only for typed planning, while deterministic code compiles governed SQL. It includes parameterized queries, hash-locked metric definitions, 11 checks, an append-only audit log, 173 backend tests and 37 live cases. | Very high | It verifies analytics, not future operational decisions. ChronosDB can own “evidence-backed counterfactual decisions.” |
| Db2 Copilot | Combines structured customer records with native Db2 vector retrieval, deterministic date calculations, SQL guardrails, query auditing, Docker Compose and adversarial tests. | High | It makes policy decisions for refunds. It does not model cascading disruption, temporal state or alternative futures. |
| DataSentry AI | Profiles datasets, detects anomalies and generates actionable data-quality reports with Db2, Gemini, LangChain.js, Node.js and React. | Medium | It monitors data quality rather than business-system resilience. |
Market conclusion

### A standard RAG agent will not stand out. The strongest competitors already demonstrate:

Db2-native retrieval
Database security
Deterministic verification
Test suites
Audit records
Exact business-rule execution
Real or realistically structured datasets

### ChronosDB must therefore compete on a different axis:

Temporal causality + counterfactual simulation + constrained optimization + decision replay

2. Why the current idea would not yet win
Current concept score
| Rubric | Current idea | Main problem |
| --- | --- | --- |
| Db2 Integration, 30 | 17/30 | Db2 is described as storage, vector search and memory, rather than the execution backbone. |
| Innovation & Impact, 25 | 18/25 | Digital-twin simulation is interesting, but “enterprise state” is too generic. |
| Architecture & AI, 20 | 15/20 | Multiple named agents do not automatically create technical depth. |
| Reproducibility & Code, 15 | 7/15 | No defined dataset, benchmark, baseline, tests or deterministic simulator. |
| Documentation & Presentation, 10 | 7/10 | The story is attractive, but the proof is not yet visible. |
| Projected total | 64/100 | Interesting concept, insufficient proof. |

The official rubric gives 30% to Db2 integration, 25% to innovation and impact, 20% to architecture, 15% to reproducibility, and 10% to documentation and presentation.

### A project can be beautiful and still lose if the judge cannot answer:

Why must this use Db2?
Which conclusions are deterministic?
How was prediction quality measured?
What does the AI do that normal SQL cannot?
What happens if the LLM is wrong?
Can I reproduce the result?
3. The winning version
Final positioning
Name
ChronosDB
Subtitle

## Auditable Counterfactual Intelligence on IBM Db2

## One-line pitch

ChronosDB turns a live supply-chain database into a decision simulator that can replay past disruptions, forecast cascading effects, compare interventions and show the exact Db2 evidence behind every recommendation.

## Judge-facing hook

“A normal dashboard tells you that a shipment is late. ChronosDB tells you what will fail next, compares three recovery plans, and proves why the selected plan is safest.”

## 4. Choose one concrete scenario

Do not build a universal enterprise digital twin. Build one excellent vertical slice.

Recommended scenario: manufacturing supply-chain disruption
Example organization

An electronics manufacturer receives components from multiple suppliers. A shipment of microcontrollers is delayed by 14 days.

### ChronosDB determines:

Which purchase orders are affected
Which bills of material depend on that component
Which production orders will stall
Which customer orders will miss service-level targets
Which alternate supplier or inventory transfer minimizes loss
The cost, delay and confidence of every option
Demo question

“Supplier S-104 will be unavailable for 14 days. What happens, and what should we do?”

## Expected output

## Baseline impact

7 production orders disrupted
3 customer SLA breaches
₹18.4 lakh estimated revenue at risk
11.6 average delay days

## Recommended intervention

Transfer 320 units from Chennai warehouse to Pune
Expedite 180 units from Supplier S-208
Reschedule Production Order PO-882 after PO-876

## Projected result

SLA breaches reduced from 3 to 1
Revenue at risk reduced by 71%
Additional logistics cost: ₹1.32 lakh
Recommendation confidence: 0.86

These should be computed from database records and simulator rules, not invented by the LLM.

5. The actual novelty
Feature 1: Temporal state reconstruction

### ChronosDB should answer:

What did the system know at 10:00 AM yesterday?
What changed between two operational snapshots?
Which state transition caused the SLA breach?
Could the breach have been prevented with the information available then?

Store event and state history in Db2 so decisions can be replayed.

Suggested tables
SUPPLIERS
COMPONENTS
BOM_DEPENDENCIES
INVENTORY_SNAPSHOTS
PURCHASE_ORDERS
PRODUCTION_ORDERS
CUSTOMER_ORDERS
DISRUPTION_EVENTS
SCENARIOS
SCENARIO_ACTIONS
SIMULATION_RUNS
SIMULATION_OUTCOMES
EVIDENCE_LINKS
AGENT_TRACES
DECISION_AUDIT

This makes Db2 central rather than decorative.

## Feature 2: Deterministic counterfactual simulator

The LLM must not calculate business outcomes.

### Use deterministic Python or SQL procedures to evaluate:

Inventory depletion
Component dependencies
Production capacity
Supplier lead time
Order priority
SLA breach
Expediting cost
Revenue at risk

### The LLM should only:

Interpret the question
Produce a typed scenario request
Explain computed results
Summarize evidence
Typed scenario request
{
  "event_type": "SUPPLIER_OUTAGE",
  "supplier_id": "S-104",
  "duration_days": 14,
  "objective": "MINIMIZE_SLA_BREACH",
  "constraints": {
    "max_extra_cost": 200000,
    "minimum_service_level": 0.90
  }
}


Reject unknown suppliers, invalid durations and malformed constraints before simulation.

## Feature 3: Constrained intervention optimization

Do not merely generate “suggestions.”

### Generate candidate interventions and calculate each outcome:

Do nothing
Transfer inventory
Use alternate supplier
Expedite shipment
Reschedule production
Combine transfer and supplier substitution

### Evaluate them using:

Utility=w1(SLA saved)−w2(additional cost)−w3(delay)−w4(risk)\text{Utility} = w_1(\text{SLA saved}) - w_2(\text{additional cost}) - w_3(\text{delay}) - w_4(\text{risk})

Save every candidate and score in Db2.

This gives judges a visible decision table rather than unverifiable prose.

## Feature 4: Evidence contract

### Every numerical claim should carry:

Metric name
Value
Unit
Scenario run ID
SQL query or stored procedure
Source rows
Calculation version
Timestamp
Confidence classification

### Example:

Revenue at risk: ₹18.4 lakh

Evidence:
SIMULATION_RUN = SR-2026-0118
Affected orders = CO-701, CO-704, CO-711
Calculation rule = revenue_at_risk_v3
Db2 records inspected = 47
Model-generated numbers = 0


This directly differentiates ChronosDB from agent demos.

## Feature 5: Decision replay

This should become the signature visual.

### The user moves a timeline from:

Before disruption
Disruption detected
Initial projection
Intervention selected
Projected recovery

### At each point, the interface shows:

Active risks
Database facts
Agent action
Simulator output
Decision
Audit record

The judge can click“Replay decision” and watch the system reconstruct the reasoning.

## 6. How to use Db2 deeply

Db2 12.1.2 introduced the native VECTOR type and vector-distance operations, while Db2 12.1.5 adds vector indexes for accelerated approximate nearest-neighbor retrieval. IBM documents vector indexes as appropriate for semantic search, recommendations, classification and other large-scale embedding workloads.

Db2 capability map
| Db2 role | Implementation | Why judges care |
| --- | --- | --- |
| System of record | Orders, suppliers, inventory, BOM and events | Demonstrates relational depth |
| Temporal evidence | Snapshot and event tables with effective timestamps | Enables replay and causality |
| Vector retrieval | Embed disruption reports, SOPs and supplier notes | Adds semantic evidence |
| Hybrid retrieval | Structured filters plus vector similarity | Better than an isolated vector database |
| Scenario persistence | Inputs, constraints, candidates and outcomes | Makes simulations auditable |
| Security | Read-only application role and restricted audit writer | Enterprise credibility |
| Auditability | Append-only decision and evidence records | Trustworthy AI |
| Analytics | Window functions, CTEs and recursive dependency traversal | Demonstrates Db2 SQL depth |
| Performance | Index query columns and benchmark vector retrieval | Reproducibility and engineering quality |

IBM’s LangChain connector supports creating vector columns, storing embeddings and performing cosine, Euclidean and dot-product searches through Python workflows.

## Important differentiation

IBM already provides runnable RAG and agentic-RAG examples featuring vector retrieval, relevance grading, query rewriting and fallback retrieval. Merely reproducing that pattern will look like a cookbook implementation, not a novel project.

### ChronosDB must go beyond retrieval by using Db2 as:

Operational state store
Scenario ledger
Evidence graph
Audit database
Evaluation store
7. Replace the five-agent theatre

The original five agents introduce complexity without guaranteed quality.

Better architecture: three controlled components
1. Scenario Planner

Produces a strict, validated scenario object.

Allowed output: JSON only
 Not allowed: calculations or recommendations

## 2. Evidence Retriever

### Retrieves:

Structured operational facts
Similar historical disruptions
Relevant SOP passages

Use Db2 relational queries plus native vector retrieval.

## 3. Decision Narrator

### Explains:

Baseline outcome
Candidate interventions
Selected intervention
Trade-offs
Uncertainty
Evidence

It cannot introduce unsupported numbers.

## Deterministic services

### Outside the LLM:

Scenario validator
Dependency resolver
Simulation engine
Constraint optimizer
Claim verifier
Audit writer

This architecture is stronger than “agents debate one another” because it reduces hallucination and can be tested.

## 8. Benchmark framework

Do not claim “90% accurate” without a defined test.

Create a benchmark with at least 30 scenario cases, preferably 50.

Scenario distribution
| Scenario type | Cases |
| --- | --- |
| Supplier outage | 10 |
| Shipment delay | 10 |
| Demand spike | 10 |
| Warehouse inventory loss | 5 |
| Production-capacity reduction | 5 |
| Multi-event disruption | 10 |
| Total | 50 |

Each synthetic scenario should have a deterministic expected outcome.

## Baselines

### Compare ChronosDB against:

## Baseline A: Naive LLM

Prompt contains a textual summary, no Db2 tools.

## Baseline B: Standard RAG

Retrieves relevant documents but does not run simulation.

## Baseline C: Rule-only simulator

Calculates outcomes but provides no semantic evidence or natural-language interface.

## ChronosDB

Relational evidence + vector retrieval + deterministic simulator + constrained optimizer + verified narration.

9. Metrics that are defensible
Correctness
| Metric | Calculation | Target |
| --- | --- | --- |
| Scenario parse success | Valid scenario objects / valid prompts | ≥95% |
| Invalid-input rejection | Correctly rejected / invalid inputs | 100% |
| Impact-set precision | Correct affected orders / predicted affected orders | ≥95% |
| Impact-set recall | Correct affected orders found / total affected orders | ≥95% |
| Numerical fidelity | Supported numerical claims / all numerical claims | 100% |
| Intervention feasibility | Feasible recommended plans / plans produced | 100% |
| Optimal-plan agreement | Selected optimal plan / benchmark-optimal plan | ≥90% |
| Citation coverage | Claims linked to evidence / verifiable claims | 100% |
Retrieval
| Metric | Target |
| --- | --- |
| Recall@5 | ≥0.85 |
| Mean Reciprocal Rank | ≥0.80 |
| Unsupported evidence rate | 0% |
| Structured filter compliance | 100% |
Performance
| Operation | Practical target |
| --- | --- |
| Scenario validation | <100 ms |
| Structured impact query | <500 ms |
| Evidence retrieval | <1 second |
| Simulation of six interventions | <2 seconds |
| End-to-end response | <8 seconds |
| Decision replay load | <2 seconds |

These are targets, not claims. Report observed median, p95 and maximum values from your actual environment.

## Safety and reliability

### Test at least:

SQL injection
Prompt injection inside an SOP document
Request to delete tables
Unknown supplier
Negative outage duration
Impossible budget
Missing inventory
Conflicting records
LLM timeout
Db2 connection failure
Unsupported numerical claim
Duplicate scenario execution

### Target:

Write attempts blocked: 100%
Unsupported numerical claims removed: 100%
Secrets in repository: 0
Critical test failures: 0
10. Judge-score projection after redesign
| Criterion | Evidence needed | Target score |
| --- | --- | --- |
| Db2 Integration, 30 | Relational operations, vectors, temporal evidence, scenarios, audit, SQL depth | 28/30 |
| Innovation & Impact, 25 | Counterfactual disruption intelligence with measurable cost and SLA impact | 23/25 |
| Architecture & AI, 20 | Typed planning, deterministic simulation, evidence verification | 18/20 |
| Reproducibility & Code, 15 | Docker setup, seeds, tests, benchmark script and one-command demo | 14/15 |
| Documentation & Presentation, 10 | Architecture, screenshots, benchmark report and polished demo | 9/10 |
| Target |  | 92/100 |

A credible 92/100 is better than claiming “102/100.” Judges reward proof, not exaggerated self-scoring.

## 11. Eye-catching interface

Use an operations war-room, not a chatbot-first design.

Main screen
Top strip
Operational health: At Risk
Revenue at risk: ₹18.4 lakh
Active disruptions: 1
Projected SLA breaches: 3
Best intervention savings: ₹13.1 lakh
Left panel: Scenario control
Supplier
Outage duration
Budget ceiling
Optimization objective
“Run counterfactual” button
Center: dependency cascade

### Show:

Supplier S-104
→ Component MCU-42
→ Production Orders PO-876 / PO-882
→ Customer Orders CO-701 / CO-704 / CO-711
→ ₹18.4 lakh at risk

Right panel: intervention comparison
Do nothing
Inventory transfer
Alternate supplier
Expedite
Hybrid plan

### Use horizontal bars for:

Cost
Delay
SLA breaches
Revenue protected
Bottom: evidence drawer
Db2 queries used
Source records
Similar historical incidents
Simulation version
Audit ID
Visual rule

The chat field should occupy no more than 20% of the first screen. The impact cascade and intervention comparison are the product.

12. Three-minute demo sequence
0:00–0:20: Establish the stakes

“A critical component supplier has failed. A dashboard can show the delay, but it cannot tell operations which orders will fail next or which intervention gives the safest recovery.”

Show the healthy supply chain turning red.

0:20–0:45: Trigger disruption

### Enter:

Supplier S-104 unavailable for 14 days. Keep recovery cost below ₹2 lakh.

Click Run counterfactual.

0:45–1:20: Show cascade

### Animate:

Supplier
Components
Production orders
Customer orders
Revenue and SLA impact

### State clearly:

“These values come from deterministic dependency and inventory calculations, not the language model.”

1:20–1:55: Compare interventions

Show five intervention cards.

### Select the best option:

71% reduction in revenue at risk
Two SLA breaches avoided
₹1.32 lakh intervention cost
1:55–2:25: Prove it

### Open the evidence drawer:

Db2 source rows
Similar incident retrieved through vector search
Calculation version
Decision audit ID
Claim verification status
2:25–2:45: Replay the past

Move the timeline backward to show what the organization knew before the disruption and when intervention became necessary.

2:45–3:00: Closing statement

“ChronosDB does not ask you to trust an AI recommendation. It lets you replay, compare and verify the decision directly against IBM Db2.”

## 13. Repository standard

The canonical submission guide expects the project under a submission folder with README.md, architecture.md, submission.json, .env.example, source code, and screenshots. It also recommends tests and provides a local validator.

chronosdb/
├── README.md
├── architecture.md
├── submission.json
├── .env.example
├── docker-compose.yml
├── Makefile
├── src/
│   ├── api/
│   ├── db/
│   ├── planner/
│   ├── retrieval/
│   ├── simulator/
│   ├── optimizer/
│   ├── verifier/
│   └── ui/
├── sql/
│   ├── 001_schema.sql
│   ├── 002_indexes.sql
│   ├── 003_seed.sql
│   └── 004_permissions.sql
├── benchmark/
│   ├── scenarios.json
│   ├── expected_outcomes.json
│   ├── run_benchmark.py
│   └── RESULTS.md
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── adversarial/
│   └── test_reproducibility.py
└── docs/
    ├── screenshots/
    ├── demo-script.md
    ├── db2-deep-dive.md
    ├── threat-model.md
    └── limitations.md

One-command requirement
make demo


### It should:

Start Db2 and the application
Create the schema
Seed the dataset
Generate or load embeddings
Run a health check
Print the local URL

The public submission instructions emphasize working source code, setup details, architecture, screenshots and a demonstration video.

## 14. What to cut

### Remove these unless they are fully implemented and measured:

Five autonomous agents
Agent debate
Multiple interchangeable LLM providers
Generic digital-twin claims
Forecast “accuracy” without ground truth
Knowledge graph terminology without an actual graph model
“Zero hallucination” unless every output class is formally controlled
Anything described only in the architecture diagram
Keep
One domain
One disruption story
One deterministic simulator
One optimizer
One evidence layer
One excellent dashboard
One benchmark suite
Final decision
Build this

ChronosDB: Auditable Counterfactual Intelligence for Supply-Chain Disruptions

## Do not build this

A generic enterprise digital twin with five conversational agents.

## Defensible differentiator

Competitors retrieve, diagnose or verify. ChronosDB reconstructs, simulates, optimizes and proves.

## Judge memory line

“ChronosDB is the Db2 time machine for enterprise decisions.”

That phrase gives the judges something short and distinctive to remember when comparing many technically strong submissions.