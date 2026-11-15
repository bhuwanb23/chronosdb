# Phase 8B: Evidence Architecture Contract

## Principle
Evidence can support decisions.
Evidence cannot create decisions.

## Retrieval Contract
```python
EvidencePackage retrieve_evidence(
    ScenarioContext context,
    Recommendation recommendation,
    RetrievalPolicy policy
)
```

## Inputs
- Supplier
- Component
- Warehouse
- Production Orders
- Disruption Type
- Intervention Type
- Region
- Dates
- Scenario Metadata

## Outputs
- Structured Facts
- Semantic Documents
- Ranking Scores
- Evidence Links
- Source Provenance

## Architectural Rule
Retrieval never changes:
- Optimization results
- Simulation results
- Business metrics

Evidence is explanatory only.

## Deliverable
docs/evidence/architecture-contract.md

## Phase 8B Status: IMPLEMENTED
