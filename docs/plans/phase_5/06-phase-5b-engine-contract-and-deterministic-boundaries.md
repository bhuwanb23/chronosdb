6. Phase 5B: Engine Contract and Deterministic Boundaries
Goal

Define the impact engine as a pure, reproducible business calculation.

Conceptual signature
Python
ImpactResult calculate_impact(
OperationalState state,
Disruption disruption,
SimulationHorizon horizon,
RuleSet rules
)
Deterministic input contract

The result may depend only on:

Operational-state version
Scenario as-of time
Disruption definition
Simulation horizon
Rule-set version
Allocation policy
Scheduling policy
Calendar configuration

The result must not depend on:

Current wall-clock time
Thread execution order
Unseeded randomness
LLM output
Network calls
Mutable global state
Database row-return order without explicit sorting
Locale-dependent date or number processing
Architectural principle

Separate:

Domain calculation

Pure calculation over typed objects.

Data access

Loads and verifies operational state.

Persistence

Stores execution records and results.

Presentation

Formats impact results for API or UI use.

The calculation layer should not contain SQL queries or HTTP concerns.

Recommended module boundaries
Plain Text
src/backend/chronosdb/impact/
├── contracts/
├── rules/
├── state/
├── disruption/
├── supply/
├── inventory/
├── materials/
├── production/
├── fulfilment/
├── financial/
├── causality/
├── provenance/
├── validation/
└── orchestration/
Deliverable
Plain Text
docs/impact-engine/engine-contract.md
