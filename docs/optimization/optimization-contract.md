# Phase 7B: Optimization Contract

## Conceptual Signature
```python
OptimizationResult optimize(
    CandidateResults simulations,
    OptimizationObjective objective,
    Constraints constraints,
    ScoringModel scoring
)
```

## Deterministic Inputs
- Simulation outputs (from Phase 6 A-V)
- Constraint set (versioned)
- Objective (explicit weights)
- Scoring version

## Must Not Depend On
- LLM ranking
- Random tie breaking
- User interface order
- Database retrieval order
- Current time

## Deliverable
docs/optimization/optimization-contract.md

## Implementation Requirements
- Deterministic output for same inputs
- Traceable provenance
- Versioned contract
- Audit trail

## Phase 7B Status: IMPLEMENTED
