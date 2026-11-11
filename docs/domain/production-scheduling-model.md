# Phase 2K: Production Scheduling Model

## MVP assumptions

- A production order has planned start and planned completion timestamps.
- Required materials must be available before production starts.
- Each facility has a daily finished-unit capacity.
- Orders use deterministic priority.
- In-progress production is not preempted.
- Setup-time optimization and machine-level scheduling are deferred.

## Scheduling calculations

Material-ready time is the latest availability time among mandatory BOM
components:

```text
material_ready_time(p) =
    max(component_available_time(p,c))
```

The result is a UTC timestamp. Preconditions are an active BOM, component
availability times for all mandatory components, and matching units. Missing
inputs produce `INSUFFICIENT_DATA`.

Capacity-ready time is the earliest time sufficient facility capacity exists,
considering in-progress work, higher-priority orders, remaining quantities, and
daily capacity.

```text
projected_start(p) =
    max(planned_start(p), material_ready_time(p), capacity_ready_time(p))
```

All three inputs are UTC timestamps and the maximum preserves the latest
constraint; no timestamp rounding is applied.

For day-bucket scheduling:

```text
duration_days(p) =
    ceil(remaining_quantity(p) / facility_daily_capacity)
projected_completion(p) =
    projected_start(p) + duration_days(p) calendar days
production_delay_hours(p) =
    max(0, projected_completion(p) - planned_completion(p))
production_delay_days(p) =
    production_delay_hours(p) / 24
```

Quantities use finished-product units, capacity uses finished units per day,
and duration uses calendar days. The day-bucket duration rounds upward once at
the duration boundary. A zero or missing facility capacity is invalid.

Internal delay remains in hours; presentation may show days without changing
the stored value.

## Scheduling outcomes

- `ON_SCHEDULE`: projected completion is no later than planned completion.
- `DELAYED`: projected completion is later.
- `BLOCKED`: a required condition cannot be determined or satisfied.
- `INSUFFICIENT_DATA`: required material, capacity, or timing fact is missing.

Completed output is preserved. A partially completed order schedules only its
remaining quantity.
