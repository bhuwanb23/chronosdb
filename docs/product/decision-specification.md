# Supplier-Outage Decision Specification

## Problem

When a critical supplier becomes unavailable, a delayed component can
propagate through inventory, production, and customer commitments. Isolated
dashboards do not consistently compare recovery actions or preserve why a
decision was made.

## Decision question

Given a supplier disruption, a selected operational state, available
interventions, and explicit constraints, which feasible intervention provides
the best outcome for the selected objective?

## MVP input contract

- supplier identifier;
- disruption start time;
- positive disruption duration;
- operational-state or as-of reference;
- affected supply or purchase-order context, when known;
- current and reserved inventory;
- component and bill-of-material relationships;
- production and customer-order commitments;
- approved supplier alternatives;
- warehouse-transfer availability;
- recovery budget and safety-stock constraints;
- facility-capacity constraints;
- optimization objective.

## MVP output contract

### Baseline

- affected components;
- shortage dates and quantities;
- affected production orders and projected delays;
- affected customer orders and projected delivery dates;
- projected SLA breaches;
- revenue at risk;
- calculation trace and rule version.

### Candidate comparison

For every candidate, preserve:

- intervention type and required actions;
- `FEASIBLE`, `INFEASIBLE`, or `INSUFFICIENT_DATA` status;
- rejection reason when not feasible;
- additional cost;
- projected delay and SLA breaches;
- revenue at risk and revenue protected;
- operational risks;
- objective score or Pareto position;
- evidence references.

### Recommendation

- selected candidate;
- active objective and constraints;
- selection explanation;
- trade-offs and remaining risks;
- scenario and simulation identifiers;
- human-review statement.

## Default objective and constraints

The MVP defaults to `MINIMIZE_SLA_BREACHES`. It must also support:

- `MINIMIZE_REVENUE_AT_RISK`;
- `MINIMIZE_TOTAL_DELAY`;
- `MINIMIZE_RECOVERY_COST`;
- `BALANCED_RECOVERY`.

Default constraints include maximum recovery cost, minimum source safety stock,
approved suppliers, available inventory, supplier capacity, and facility
capacity.

## Authority and responsibility

Deterministic Python/SQL owns business calculations. A future language model
may interpret input or explain verified results, but may not change scores,
feasibility, evidence, or numerical outputs. The user approves and executes
the final operational action.
