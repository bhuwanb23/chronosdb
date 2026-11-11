# Product Acceptance Tests

These tests define behavior before implementation. Exact golden-scenario
numbers are inputs to be frozen during Phases 2 and 3.

## AT-001 Valid supplier outage

Given an active supplier with a known component relationship, when the user
submits a positive 14-day outage with objective and constraints, then the
scenario is accepted, receives an ID, stores its state reference, and remains
immutable after execution starts.

## AT-002 Unknown supplier

Given an unknown supplier ID, when a scenario is submitted, then execution
does not begin, an `UNKNOWN_SUPPLIER` error is returned, and validation failure
is audited.

## AT-003 Do-nothing impact

Given the frozen golden scenario, when baseline impact is calculated, then
affected components, production orders, customer orders, delay, SLA breaches,
and revenue at risk exactly match the approved expected outcomes and retain a
calculation trace.

## AT-004 Safety-stock violation

Given a warehouse whose stock would fall below its transfer threshold, when an
inventory-transfer candidate is evaluated, then it is marked infeasible with
`SOURCE_SAFETY_STOCK_VIOLATION`.

## AT-005 Budget violation

Given a candidate whose cost exceeds the scenario budget, then it is not
eligible for recommendation, retains its infeasibility reason, and does not
silently disappear from comparison.

## AT-006 Unapproved alternate supplier

Given an alternate supplier without approval for the component, then the
candidate is never recommended and the rejection reason is visible.

## AT-007 LLM unavailable

Given that any future LLM service is unavailable, then structured input,
deterministic calculation, candidate comparison, evidence, audit, and a
templated summary still work.

## AT-008 Unsupported numerical claim

Given a narrator output containing a number absent from verified structured
results, then verification fails, the number is removed or narration is
regenerated, and the failure is audited.

## AT-009 Scenario isolation

Given two scenarios sharing a baseline but using different disruptions, then
running one cannot mutate the other scenario, its inputs, or its results.

## AT-010 Decision replay

Given a completed scenario, when it is replayed, then the stored decision
state, rule version, results, and evidence links are reproduced without
recalculation or mutation.

## AT-011 No feasible intervention

Given an outage where every candidate violates a hard constraint, then the
system returns `NO_FEASIBLE_INTERVENTION` and does not recommend the
least-invalid option.

## AT-012 Insufficient data

Given a missing inventory snapshot, conflicting supplier capacity, or missing
customer due date, then the affected result returns `INSUFFICIENT_DATA` and
does not treat missing information as zero.

## Coverage rule

AT-001 through AT-006 cover the Priority 0 scenario, impact, intervention, and
constraint groups. AT-007 through AT-012 cover reliability, safety, audit, and
degraded behavior. Each test must later receive an automated test ID and a
fixture or golden-data reference.
