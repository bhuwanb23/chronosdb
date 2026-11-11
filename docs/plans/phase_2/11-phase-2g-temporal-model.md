11. Phase 2G: Temporal Model
Goal

Define exactly which time each record represents and how historical state is reconstructed.

11.1 Time dimensions
Event time

When something happened in the business world.

Example:

Plain Text
Supplier outage begins at 2026-11-11 08:00 IST
Reported time

When ChronosDB learned about an event.

Example:

Plain Text
Outage reported at 2026-11-11 09:15 IST
Ingestion time

When the record entered Db2.

Effective time

When a business record is considered valid.

Scenario as-of time

The point at which operational state is frozen for simulation.

Simulation horizon

The future interval over which impact is calculated.

11.2 Clock standard

Store canonical timestamps in UTC.

Display local time using:

Plain Text
Asia/Kolkata

The time zone must be attached to user-facing dates or documented globally.

11.3 Effective interval

Use:

[effective_from,effective_to)[effective\_from, effective\_to)[effective_from,effective_to)

A record is active at time ttt when:

effective_from≤t<effective_toeffective\_from \le t < effective\_toeffective_from≤t<effective_to

If effective_to is absent, the interval remains open.

11.4 Scenario state rule

The scenario uses records known and valid at its as_of_time.

Conceptually:

State(t)={r∣r.valid_at(t)∧r.known_by(t)}State(t) = \{r \mid r.valid\_at(t) \land r.known\_by(t)\}State(t)={r∣r.valid_at(t)∧r.known_by(t)}

For the MVP, avoid retroactive data corrections unless explicitly modelled.

11.5 Planning granularity

Use one-hour granularity for operational timestamps.

Business lead times may be expressed in days but converted to hours:

LeadTimeHours=LeadTimeDays×24LeadTimeHours = LeadTimeDays \times 24LeadTimeHours=LeadTimeDays×24

If working-day calendars are not implemented, explicitly state that lead times use elapsed calendar time.

11.6 Simulation horizon

Recommended golden scenario:

Plain Text
30 calendar days

The horizon must exceed the outage duration and expected recovery period.

11.7 Late-arriving data

If a record is ingested after scenario freeze:

It must not silently change the completed scenario.
A new scenario or state version is required.
Replay must preserve the original information state.
Deliverables
Plain Text
docs/domain/temporal-model.md
docs/domain/time-examples.md
Temporal acceptance tests
A BOM version ending at 10:00 is not active at 10:00.
The next BOM version beginning at 10:00 is active at 10:00.
A late-ingested disruption does not modify an earlier completed scenario.
An order received before the outage is not treated as outstanding supply.
A replenishment arriving after a shortage can resolve later demand but not earlier missed demand.
