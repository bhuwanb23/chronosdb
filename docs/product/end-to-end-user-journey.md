# End-to-End User Journey

## Journey overview

```text
Select state
  -> Define supplier outage
  -> Define constraints
  -> Create immutable scenario
  -> Calculate do-nothing impact
  -> Generate and validate candidates
  -> Simulate and compare
  -> Review recommendation
  -> Inspect evidence
  -> Replay decision
```

## Stages and contracts

### 1. Select operational state

The user selects the current state or a historical as-of timestamp.

Success: the system identifies the exact state reference.

Failure: history is unavailable, the timestamp predates retained data, or
effective dates conflict. The system stops before creating a scenario.

### 2. Define disruption

The user enters supplier ID, start time, positive duration, optional affected
purchase orders, and notes.

Success: a typed, validated supplier-outage request exists.

Failure: unknown supplier, no active component relationship, invalid start time,
non-positive duration, or missing required field.

### 3. Define constraints

The user selects an objective and enters budget, safety-stock, supplier,
inventory, and capacity constraints.

Success: constraints are explicit and inspectable.

Failure: negative budget, impossible limit, unsupported objective, or conflicting
constraints.

### 4. Create immutable scenario

ChronosDB stores the request, state reference, constraints, objective,
creation time, scenario ID, and rule version. The input cannot be silently
changed after execution begins.

### 5. Calculate do-nothing impact

The system calculates the dependency cascade from supplier to component,
inventory, production, and customer commitments. It returns shortages, delays,
SLA exposure, revenue at risk, and a calculation trace.

Failure: incomplete or conflicting operational data is surfaced as
`INSUFFICIENT_DATA`; it is not silently filled in.

### 6. Generate and validate candidates

Candidates include do nothing, inventory transfer, shipment expedition,
approved alternate supplier, production rescheduling, and optionally a hybrid.
Each candidate remains visible with `FEASIBLE`, `INFEASIBLE`, or
`INSUFFICIENT_DATA` status and a reason.

### 7. Simulate and compare

Each feasible candidate runs against the same immutable baseline. The user
compares cost, delay, SLA breaches, revenue at risk, revenue protected, and
operational risk.

### 8. Review recommendation

ChronosDB identifies the highest-ranked feasible candidate for the selected
objective and displays the constraints, trade-offs, warnings, and human-review
statement. It does not execute the action.

### 9. Inspect evidence

The user can open source Db2 records, calculation traces, rule version,
simulation run, and relevant controlled documents when available.

### 10. Replay decision

The user can review the stored stages from initial state through final audit
snapshot without changing the original scenario or result.

## Degraded operation

- If Db2 is unavailable, the request fails safely and exposes no credentials.
- If operational data is incomplete, the affected candidate/result is marked
  `INSUFFICIENT_DATA`.
- If a future LLM is unavailable, structured input, deterministic calculation,
  comparison, evidence, and a templated summary remain available.
- If one candidate fails, successful candidates remain reviewable.
