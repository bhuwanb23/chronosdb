# Phase 2Q: Provenance Model

## Evidence categories

### Operational evidence

Supplier agreements, purchase orders, inventory snapshots, BOM versions,
production orders, and customer orders.

### Rule evidence

Formula ID, allocation rule, scheduling rule, feasibility rule, objective
version, and business-rule version.

### Contextual evidence

Disruption reports, recovery procedures, and historical incidents. Contextual
documents explain or support decisions but cannot create current operational
facts.

### Execution evidence

Scenario ID, simulation-run ID, input-state version, rule version, timestamp,
and system version.

## Provenance chain

```text
Displayed claim
  -> derived output field
  -> calculation step
  -> formula/rule ID
  -> input records
  -> state version
  -> scenario and simulation run
```

## Presentation contract

A result is presentation-ready only when it identifies:

- source records;
- formula and rule version;
- scenario and simulation run;
- value and unit;
- reference case for a delta;
- evidence category and status.

## Golden target

`provenance_coverage = complete key outputs / all key outputs`

The corrected golden scenario target is 100%. A missing link is surfaced as
incomplete evidence; it is not replaced with a fabricated citation.
