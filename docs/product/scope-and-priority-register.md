# Scope and Priority Register

## Locked vertical slice

ChronosDB first supports one workflow:

```text
Critical supplier outage
 -> dependency impact
 -> do-nothing baseline
 -> feasible recovery comparison
 -> human-reviewed recommendation
 -> evidence and audit trail
```

## Priority 0 — required core

- Accept and validate a structured supplier outage.
- Load a specified operational state from Db2.
- Calculate do-nothing impact through components, inventory, production, and
  customer commitments.
- Evaluate inventory transfer, shipment expedition, approved alternate
  supplier, and production rescheduling.
- Compare at least five candidates including do nothing.
- Select the best feasible candidate for an explicit objective.
- Display source evidence and preserve an audit record.
- Produce a deterministic summary and documented setup path.

## Priority 1 — supporting capabilities

- Natural-language scenario creation with typed validation.
- Db2-native semantic and structured evidence retrieval.
- Historical incident retrieval.
- Evidence drawer and decision replay.
- Numerical claim verification.
- Hybrid intervention.
- Baseline-versus-recommendation visualization.

## Priority 2 — differentiators

- Pareto frontier.
- Sensitivity analysis.
- Historical as-of state reconstruction.
- Scenario duplication.
- Timeline replay.
- Confidence classification based on data completeness.
- Downloadable decision report.

## Priority 3 — deferred

Demand spikes, warehouse closures, production-line outages, multi-event
disruptions, Monte Carlo simulation, geographic routing, live ERP connectors,
autonomous agents, multiple LLM providers, automatic purchase-order execution,
and real external supplier feeds.

## Scope-change rule

A proposed feature may enter the active scope only when it:

1. serves a documented user need;
2. has known data and evidence requirements;
3. has defined failure behavior;
4. has acceptance-test coverage;
5. does not delay unfinished Priority 0 work;
6. has an owner and decision record.

Otherwise it remains deferred. A feature priority is not changed merely because
it is visually attractive or easy to demo.
