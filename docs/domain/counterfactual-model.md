# Phase 2O: Counterfactual Scenario Model

## Composition

```text
Scenario =
  baseline state
  + disruption
  + objective
  + constraints
  + simulation horizon
  + rule version

Counterfactual run = scenario + one intervention overlay
```

## State layers

1. **Operational state:** factual state at scenario `as_of_time`; immutable.
2. **Disruption overlay:** changed expected future supply; shared by candidates.
3. **Intervention overlay:** changed receipts, transfers, allocation, or
   schedule for one candidate.
4. **Derived outcome:** shortages, delays, SLA breaches, cost, and financial
   impact for that run.

Layer 1 and Layer 2 are immutable during all runs. Each Layer 3 overlay is
isolated. Layer 4 belongs to one scenario and simulation run.

## Comparability

All candidates in one comparison use the same:

- baseline state version;
- disruption;
- simulation horizon;
- business-rule version;
- objective definitions;
- cost basis.

If any differs, the outcomes are not comparable and the comparison must be
rejected.

## Determinism

Identical `baseline_state_version`, disruption, intervention, constraint set,
and rule version produce identical outcomes. Randomness is not part of the MVP.

## Outcome deltas

For candidate `i`, relative to the do-nothing case:

```text
revenue_protected(i) =
    max(0, revenue_at_risk(do_nothing) - revenue_at_risk(i))

sla_breaches_avoided(i) =
    sla_breaches(do_nothing) - sla_breaches(i)

delay_reduction(i) =
    total_delay(do_nothing) - total_delay(i)
```

Every delta names its reference case, unit, scenario, and simulation run.

## Invariants

- Operational facts cannot be modified by a scenario.
- An intervention cannot create material from nothing.
- A run cannot read another candidate's overlay.
- Every output has scenario and run identity.
- Failed candidates do not invalidate successful candidates.
