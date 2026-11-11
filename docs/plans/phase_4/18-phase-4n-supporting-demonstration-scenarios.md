18. Phase 4N: Supporting Demonstration Scenarios
Goal

Show that ChronosDB is a system rather than a single hardcoded path.

Create at least five polished supporting scenarios.

DEMO-002: No-impact outage

A supplier outage occurs, but projected inventory covers all demand.

Expected:

Plain Text
Supply disruption detected
Operational shortage: None
SLA breaches: 0
Recommended action: Monitor, no intervention required
DEMO-003: No feasible recovery
No transferable stock
No approved alternate supplier
Expedition unavailable
Budget insufficient

Expected:

Plain Text
NO_FEASIBLE_INTERVENTION

The system must not recommend an invalid plan.

DEMO-004: Budget trade-off
Hybrid intervention prevents all breaches but exceeds budget.
Transfer-only intervention is feasible but leaves one breach.

Expected:

Plain Text
Recommendation respects budget.
Excluded hybrid remains visible with reason.
DEMO-005: Priority conflict

Rescheduling protects a low-value order but delays a strategic customer.

Expected:

Externality is shown.
Strategic priority affects ranking.
Rescheduling is not presented as a free improvement.
DEMO-006: Insufficient data

An inventory snapshot is missing.

Expected:

Plain Text
INSUFFICIENT_DATA

The system must not infer zero inventory.

DEMO-007: Historical replay

A late inventory correction becomes known after the original scenario.

Expected:

Original scenario keeps original state.
New scenario uses corrected information.
Difference is visible and auditable.
Deliverables
Plain Text
data/releases/v1.0.0/demo-scenarios/
