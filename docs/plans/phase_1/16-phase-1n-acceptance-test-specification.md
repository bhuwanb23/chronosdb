16. Phase 1N: Acceptance-test specification
Goal

Define product-level tests before implementation.

AT-001: Valid supplier outage
Given
Supplier S-104 exists.
It supplies critical component C-042.
The user provides a 14-day outage.
When

The scenario is created.

Then
Scenario is accepted.
A unique ID is assigned.
Start date and duration are stored.
Objective and constraints are preserved.
Original input remains immutable.
AT-002: Unknown supplier
Given

Supplier S-999 does not exist.

## When

The user creates a scenario.

Then
Scenario execution does not begin.
Error code identifies an unknown supplier.
No simulation record is created.
An audit event records validation failure.
AT-003: Do-nothing impact
Given

A frozen golden scenario.

## When

The baseline is calculated.

## Then

## Results exactly match:

Expected affected components
Expected affected production orders
Expected customer orders
Expected delay
Expected SLA breaches
Expected revenue at risk

Exact values will be defined in Phases 2 and 3.

AT-004: Safety-stock violation
Given

A warehouse has surplus stock above zero but below the transferable threshold.

## When

An inventory-transfer candidate is evaluated.

## Then

## The candidate is marked infeasible with:

## SOURCE_SAFETY_STOCK_VIOLATION

AT-005: Budget violation
Given

An intervention costs more than the scenario budget.

## Then

It is marked infeasible or excluded from selection, but its projected operational result remains available for comparison if calculated.

## AT-006: Alternate supplier not approved

An unapproved supplier must never be recommended.

## AT-007: LLM unavailable

The deterministic workflow continues and produces a templated report.

## AT-008: Unsupported numerical claim

## If the narrator emits a value not present in structured results:

Verification fails.
The value is removed or the narrative is regenerated.
The failure is audited.
AT-009: Scenario isolation

Two scenarios using the same baseline but different outages must not modify one another.

## AT-010: Decision replay

Loading a completed scenario must reproduce the stored decision state and original evidence links.

## AT-011: No feasible intervention

## The system returns:

## NO_FEASIBLE_INTERVENTION


It must not recommend the least-invalid option.

## AT-012: Insufficient data

## Missing information required for calculation returns:

## INSUFFICIENT_DATA


It must not be treated as zero.

Deliverable
docs/product/product-acceptance-tests.md

## Exit gate

At least one acceptance test exists for every Priority 0 requirement group.

