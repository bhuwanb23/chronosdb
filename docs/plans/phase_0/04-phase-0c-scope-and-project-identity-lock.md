4. Phase 0C: Scope and Project Identity Lock
Goal

Prevent architecture drift, naming inconsistency and feature expansion.

Locked identity
Project name: ChronosDB
Descriptive name: ChronosDB: Auditable Counterfactual Intelligence
Domain: Supply-chain disruption decision intelligence
Primary scenario: Critical supplier outage
Database: IBM Db2
AI framework: LangChain
Backend: Python + FastAPI
Frontend: React-based web interface
Primary user: Supply-chain operations manager


LangChain is the recommended qualifying framework because it can support typed planning and retrieval without forcing the simulation engine into an agent framework. This lets deterministic Python and SQL retain authority over business calculations.

### Subphase 0C.1: Product charter

### Create:

docs/project-control/product-charter.md


### It must include:

## Problem

Operations teams can observe disruptions but struggle to trace cascading impacts and compare auditable recovery plans.

## Product promise

ChronosDB reconstructs supply-chain state, simulates alternative interventions and proves every recommendation using Db2 evidence.

In scope
Supplier outage
Inventory projection
BOM dependency propagation
Production delay
Customer SLA impact
Revenue at risk
Intervention comparison
Db2 evidence
Decision audit
Out of scope for MVP
Live ERP integration
Real-time external news
Multi-company collaboration
Autonomous purchasing
Monte Carlo forecasts
Geographic route optimization
Multiple LLM providers
Agent debate
Direct production actions
Subphase 0C.2: Terminology lock

### Define exact meanings:

revenue_at_risk, not revenue lost
projected_delay_days, not confirmed delay
recommended_intervention, not autonomous decision
simulation, not prediction unless a predictive model exists
confidence, only when mathematically defined
evidence, only when linked to a source record
Exit criterion

No major project description should use language that exceeds implemented capability.

