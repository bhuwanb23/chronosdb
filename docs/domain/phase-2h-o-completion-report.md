# Phase 2H–2O Completion Report

## Scope

Phase 2H–2O is complete as a conceptual domain-rules package. No Db2 schema,
SQL migration, seed data, simulator, optimizer, API, UI, vector retrieval, or
AI prompt was added.

## Completed gates

| Area | Result |
|---|---|
| Supplier outage parameters and scope | Pass |
| Outage boundaries and recovery lag | Pass |
| Inventory balance and usable quantity | Pass |
| Reservation and allocation policy | Pass |
| Shortage and transfer rules | Pass |
| BOM selection and requirements | Pass |
| Production material/capacity scheduling | Pass |
| Customer fulfilment and partial quantity | Pass |
| SLA and revenue-at-risk semantics | Pass |
| Causal edges and trace format | Pass |
| Intervention parameters and feasibility codes | Pass |
| Counterfactual isolation and comparability | Pass |
| H–O formula metadata and failure states | Pass |

## Paper consistency checks

### Normal supplier outage

An `ALL_SUPPLY` outage delays only outstanding affected supply by outage end
plus configurable recovery lag. Inventory balances incorporate the delayed
receipt, allocation follows deterministic priority, mandatory BOM shortages
delay production, and customer impact uses late quantity rather than full-order
revenue.

### Safety-stock and transfer failure

A transfer exceeding source transferable quantity is rejected with a
machine-readable code. Production may consume below safety stock when
necessary, but an optional transfer may not cross the protected source
threshold.

### Missing BOM

No BOM active at production start returns `INSUFFICIENT_DATA`; the model does
not select the latest version or treat demand as zero.

### Capacity delay

Projected start is the maximum of planned start, material-ready time, and
capacity-ready time. Day-bucket duration is explicit and stable priority
resolves ties.

### Partial customer fulfilment

On-time fulfilled quantity is separated from late quantity. Revenue at risk is
late quantity times unit revenue, and order-line and order-level breach counts
remain distinct.

### Infeasible intervention

A hard-constraint violation produces `INFEASIBLE` with a rejection code. Missing
facts produce `INSUFFICIENT_DATA`; unsupported intervention types produce
`UNSUPPORTED`.

### Shared baseline with two candidates

Both candidates use the same immutable operational state, disruption, horizon,
rule version, objective, and cost basis. Each intervention overlay is isolated,
so one run cannot affect the other.

### Formula metadata review

The H–O formulas identify their quantity or time units, non-negative and
valid-state preconditions, rounding boundaries, and
`INSUFFICIENT_DATA`/invalid-input behavior. No formula silently converts units,
rounds intermediate values, or treats missing data as zero.

## Deferred Phase 2 work

Phase 2P–2V still owns the formula catalogue, provenance, uncertainty and data
quality, golden scenario, domain benchmark, falsification review, and Phase 3
handoff. H–O rules must not be considered fully implemented until those later
sections are complete.

## Gate result

**Phase 2H–2O: PASS.** The disruption-to-counterfactual domain rules are
defined consistently enough for the remaining formula, provenance, uncertainty,
golden-scenario, and benchmark work.
