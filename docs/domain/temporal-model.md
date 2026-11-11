# Phase 2G: Temporal Model

## Time dimensions

| Dimension | Meaning | Example |
|---|---|---|
| Event time | When the business event occurred | Outage begins at 08:00 |
| Reported time | When the organization learned of it | Reported at 09:15 |
| Ingestion time | When the record entered the system | Loaded at 09:20 |
| Effective time | When a business record is valid | Agreement starts at 00:00 |
| As-of time | Point at which scenario state is frozen | Scenario reads 09:00 state |
| Simulation horizon | Future interval being projected | Next 30 calendar days |

These dimensions must not be collapsed into one timestamp.

## Clock and display

Canonical timestamps are stored conceptually in UTC. User-facing timestamps
use `Asia/Kolkata` and must include the zone or be accompanied by a documented
display-zone label.

Operational planning uses one-hour granularity for the MVP. Lead times stated
in days use elapsed calendar time:

`lead_time_hours = lead_time_days * 24`

Working-day calendars are deferred.

## Effective intervals

Versioned records use a half-open interval:

```text
[effective_from, effective_to)
```

A record is active at time `t` when:

```text
effective_from <= t < effective_to
```

An absent `effective_to` means the interval is open. At a boundary, the ending
version is inactive and the version beginning at that exact instant is active.
Overlapping active versions for the same business key are invalid unless a
later rule explicitly defines priority.

## Historical state rule

For scenario as-of time `t`, the operational state is:

```text
State(t) = { record | valid_at(record, t) and known_by(record, t) }
```

`valid_at` uses effective intervals. `known_by` uses the information/reporting
time appropriate to the record. This prevents later knowledge from leaking
into an earlier decision replay.

## Scenario freeze and late data

Once a scenario is frozen, later-ingested or retroactively corrected records
cannot silently change it. The system must create a new state version or a new
scenario. Replay uses the original information state and rule version.

## Horizon

The golden scenario uses a recommended 30-calendar-day simulation horizon. The
horizon must exceed the outage duration and expected recovery period. Events
outside the horizon may be stored but do not affect the scenario result unless
the result explicitly reports a horizon boundary.

## Temporal invariants

- A replenishment cannot be consumed before its arrival time.
- A purchase order received before outage start is not affected by that outage.
- A BOM ending at a boundary is not active at the boundary.
- A BOM beginning at the boundary is active at the boundary.
- A late-arriving record cannot alter a completed scenario.
- A replenishment after a shortage can resolve later demand, not earlier missed
  demand.
