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

