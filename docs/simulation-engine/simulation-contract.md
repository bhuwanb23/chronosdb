# Simulation Contract

## Conceptual Signature

```python
SimulationResult simulate(
    OperationalState state,
    Disruption disruption,
    InterventionOverlay overlay,
    RuleSet rules,
    Horizon horizon
)
```

## Deterministic Inputs

Simulation must depend only on:

- state hash
- disruption definition
- overlay definition
- horizon
- rule set
- allocation policy
- scheduling policy

## Must Not Depend On

- current time
- thread scheduling
- randomness
- LLM output
- network requests
- user interface state

## Principle

Phase 6 reuses Phase 5 inventory, allocation, scheduling, and financial logic. Phase 6 is a state modifier plus impact engine runner; it does not rewrite operational logic.