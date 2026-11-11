# Phase 2E: State and Lifecycle Model

Statuses describe operational or analytical state. A simulation may project a
status but must not mutate the source operational record.

## Scenario

```text
DRAFT -> VALIDATED -> FROZEN -> SIMULATING -> COMPLETED
  \-> REJECTED       \-> REJECTED
                       SIMULATING -> PARTIALLY_COMPLETED
                       SIMULATING -> FAILED
```

- `DRAFT`: inputs are editable and incomplete.
- `VALIDATED`: required references and constraints pass validation.
- `FROZEN`: inputs and state reference are immutable.
- `SIMULATING`: one or more runs are executing.
- `COMPLETED`: all required runs completed.
- `PARTIALLY_COMPLETED`: some runs completed and others failed.
- `FAILED`: no usable run completed.
- `REJECTED`: validation prevented execution.

Only `VALIDATED` may become `FROZEN`. Re-running creates a new simulation run.

## Purchase order

```text
DRAFT -> CONFIRMED -> IN_TRANSIT -> PARTIALLY_RECEIVED -> RECEIVED
                         \-> DELAYED
DRAFT/CONFIRMED/IN_TRANSIT -> CANCELLED
```

Only outstanding quantity is exposed to a disruption:

`outstanding = max(0, ordered quantity - received quantity)`

Received quantity and cancelled quantity are never delayed by simulation.

## Production order

```text
PLANNED -> RELEASED -> IN_PROGRESS -> COMPLETED
    \-> BLOCKED
    \-> DELAYED
PLANNED/RELEASED -> CANCELLED
```

Completed quantity is never undone. The remaining quantity is evaluated.
In-progress orders retain already consumed material; planned orders compete for
future material according to priority.

## Customer order

```text
OPEN -> ALLOCATED -> IN_PRODUCTION -> READY -> SHIPPED -> DELIVERED
  \-> DELAYED
OPEN/ALLOCATED -> CANCELLED
```

`DELAYED` is a projected or operational service state and must retain the
original promised delivery time.

## Intervention

```text
GENERATED -> VALIDATING -> FEASIBLE -> SIMULATED -> RANKED -> RECOMMENDED
                 \-> INFEASIBLE
                 \-> INSUFFICIENT_DATA
                          SIMULATED -> SIMULATION_FAILED
```

`INFEASIBLE` means a known hard constraint fails. `INSUFFICIENT_DATA` means a
required fact is missing or conflicting. They are never interchangeable.

## Transition invariants

- Every transition has a trigger and entry condition.
- Frozen scenario inputs cannot change.
- A failed candidate cannot erase successful candidates.
- A recommendation is reviewable, not executed.
- Operational completion cannot be reversed by a counterfactual run.
