7. Phase 1E: End-to-end user journey
Goal

Specify the complete user experience before APIs and screens are designed.

## Journey stage 1: Select operational state

## The user chooses:

Current operational state, or
Historical as-of timestamp
Result

ChronosDB identifies which version of supply-chain data should be used.

Failure cases
Timestamp predates available history
Required snapshot unavailable
Some records have conflicting effective dates
Journey stage 2: Define disruption

## The user enters:

Event type: supplier outage
Supplier identifier
Start time
Duration
Optional affected purchase orders
Operational notes

## Example:

Supplier S-104 is unavailable for 14 days beginning 11 November.

## Result

A validated scenario request is created.

Failure cases
Supplier does not exist
Supplier has no active component relationship
Duration is negative
Start date is invalid
Required field is missing
Journey stage 3: Define constraints

## The user enters:

Maximum recovery budget
Minimum service level
Safety-stock policy
Optimization objective
Optional intervention exclusions

## Example:

Maximum recovery cost: ₹200,000
Objective: Minimize SLA breaches
Do not use unapproved suppliers

## Journey stage 4: Create immutable scenario

## ChronosDB stores:

Scenario inputs
Operational-state reference
Constraint set
User-selected objective
Creation time
Scenario ID
Rule version

Once simulation begins, the original scenario input cannot be silently changed.

## Journey stage 5: Calculate do-nothing impact

ChronosDB calculates the consequence of taking no intervention.

## The user sees:

Dependency cascade
Shortage timeline
Affected production orders
Affected customer orders
SLA exposure
Revenue at risk
Journey stage 6: Generate candidate interventions

## ChronosDB creates candidates such as:

Do nothing
Transfer inventory from another warehouse
Expedite an existing shipment
Use an approved alternate supplier
Reschedule production
Use a hybrid recovery plan
Journey stage 7: Validate candidates

## Each candidate is checked against:

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

## Journey stage 8: Simulate candidates

## For every feasible intervention, ChronosDB calculates:

New inventory projection
New production completion
New customer delivery projection
New SLA count
New revenue-at-risk value
Additional cost
Journey stage 9: Compare alternatives

## The user compares:

Do nothing
Cheapest intervention
Best service-level intervention
Lowest-delay intervention
Balanced recommendation
Journey stage 10: Review recommendation

## ChronosDB explains:

Why the intervention was selected
Which constraints affected selection
Which outcome improved
What additional cost is required
Which risks remain
Which evidence was used
Journey stage 11: Inspect evidence

## The user can open:

Source Db2 records
Calculation trace
Historical incident
Relevant operating procedure
Rule version
Simulation run
Decision audit record
Journey stage 12: Replay decision

## The user can move through:

Initial operational state
Disruption introduced
Baseline impact
Candidate generation
Candidate simulation
Recommendation
Final audit snapshot
Deliverable
docs/product/end-to-end-user-journey.md

## Benchmark

## Every journey step must map to:

At least one functional requirement
At least one success condition
At least one failure behavior
At least one future test

## Target coverage:

100%

