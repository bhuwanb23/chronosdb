# Phase 2G: Time Examples

## Example 1: Effective-date boundary

Two BOM versions exist for product `P-100`:

- version 1: `[2026-11-01T00:00Z, 2026-11-11T10:00Z)`;
- version 2: `[2026-11-11T10:00Z, open)`.

At exactly `10:00Z`, version 1 is inactive and version 2 is active. A request
for the state at `09:59Z` selects version 1.

## Example 2: Information-time boundary

A supplier outage begins at `08:00 IST`, is reported at `09:15 IST`, and is
ingested at `09:20 IST`.

- A scenario as of `09:00` cannot use the outage as known information.
- A scenario as of `09:30` may use it, provided the event is effective for that
  state.
- A later correction cannot mutate the completed `09:30` scenario.

## Example 3: Replenishment after shortage

A component requirement is due at 12:00. The supplier receipt arrives at 18:00.
The receipt may satisfy a later requirement, but the 12:00 requirement remains
late and contributes to the projected impact.

## Example 4: Outage boundaries

An outage runs from 11 November 08:00 through 25 November 08:00.

- Quantity received at 07:59 on 11 November is protected.
- Outstanding quantity expected at 12:00 on 11 November is affected.
- A purchase order arriving after the outage may remain unaffected if normal
  capacity permits it.
- The configurable recovery lag begins after outage end.

## Example 5: Planning granularity

A two-day lead time becomes 48 elapsed hours. A start at
`2026-11-11T08:00Z` projects arrival at `2026-11-13T08:00Z`. No working-day
calendar is assumed in the MVP.

## Example 6: State reconstruction

For an as-of time, select records that are both valid at that time and known by
that time. A record valid today but ingested after the as-of time is excluded
from the historical state.
