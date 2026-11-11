8. Phase 1F: Use-case catalogue
Goal

Create formal use cases with preconditions, triggers, flows and outcomes.

UC-001: Create supplier-outage scenario
Actor

## Supply-chain operations manager

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

## UC-003: Generate intervention candidates

## Candidate set:

Inventory transfer
Shipment expedition
Alternate supplier
Production rescheduling
Hybrid intervention
Postcondition

## Every candidate is marked:

FEASIBLE
INFEASIBLE
INSUFFICIENT_DATA

## UC-004: Compare intervention outcomes

The system presents comparable metrics using the same units and baseline.

## UC-005: Recommend an intervention

The system selects the highest-ranking feasible candidate under the selected objective.

## UC-006: Inspect evidence

The user can follow each major result to its source records and calculation trace.

## UC-007: Replay an earlier decision

The user can load a completed scenario without recomputing or changing its original result.

## UC-008: Handle insufficient data

## The system must distinguish:

NO_IMPACT
NO_FEASIBLE_INTERVENTION
INSUFFICIENT_DATA
SIMULATION_FAILED


These are not equivalent states.

## UC-009: Operate without LLM service

## The system must still:

Accept a structured scenario
Run deterministic calculations
Compare interventions
Display a templated summary
Preserve evidence

Natural-language parsing and narration may be unavailable.

Deliverable
docs/product/use-case-catalogue.md

## Exit criteria

## Each use case contains:

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
