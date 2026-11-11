9. Phase 2E: State and Lifecycle Model
Goal

Define valid status values and state transitions.

9.1 Scenario lifecycle
Plain Text
DRAFT
→ VALIDATED
→ FROZEN
→ SIMULATING
→ COMPLETED

Failure transitions:

Plain Text
DRAFT → REJECTED
VALIDATED → REJECTED
SIMULATING → PARTIALLY_COMPLETED
SIMULATING → FAILED

Rules:

Only a validated scenario may be frozen.
Frozen scenario inputs are immutable.
Re-running creates a new simulation run.
Failure must not modify original input.
9.2 Purchase-order lifecycle
Plain Text
DRAFT
→ CONFIRMED
→ IN_TRANSIT
→ PARTIALLY_RECEIVED
→ RECEIVED

Alternative states:

Plain Text
CANCELLED
DELAYED

Only outstanding quantity is affected by an outage.

Qoutstanding=max⁡(0,Qordered−Qreceived)Q_{outstanding} = \max(0, Q_{ordered} - Q_{received})Qoutstanding​=max(0,Qordered​−Qreceived​)
9.3 Production-order lifecycle
Plain Text
PLANNED
→ RELEASED
→ IN_PROGRESS
→ COMPLETED

Alternative states:

Plain Text
BLOCKED
DELAYED
CANCELLED
MVP disruption treatment
Completed quantity is not undone.
Only the uncompleted portion is evaluated.
An in-progress order may already have consumed allocated materials.
Planned orders compete for future material.
9.4 Customer-order lifecycle
Plain Text
OPEN
→ ALLOCATED
→ IN_PRODUCTION
→ READY
→ SHIPPED
→ DELIVERED

Alternative states:

Plain Text
DELAYED
CANCELLED
9.5 Intervention lifecycle
Plain Text
GENERATED
→ VALIDATING
→ FEASIBLE
→ SIMULATED
→ RANKED
→ RECOMMENDED

Alternative states:

Plain Text
INFEASIBLE
INSUFFICIENT_DATA
SIMULATION_FAILED
Deliverable
Plain Text
docs/domain/state-transition-model.md
Exit gate
Every state has an entry condition.
Every transition has a valid trigger.
Terminal and recoverable failures are separated.
Completed operational work cannot be reversed by simulation.
Insufficient data is not treated as infeasibility.
