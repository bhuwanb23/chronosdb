# Phase 2B: Bounded Context

## Context name

**Manufacturing supply-chain disruption planning**

ChronosDB models the planning decision from supplier procurement through
inbound replenishment, warehouse inventory, material allocation, production
fulfilment, and customer-order delivery.

```text
Supplier procurement
  -> Inbound replenishment
  -> Warehouse inventory
  -> Material allocation
  -> Production fulfilment
  -> Customer delivery
```

## In scope

- approved supplier/component relationships;
- inbound purchase orders and expected receipts;
- component inventory and reservations;
- product BOMs and material requirements;
- production orders and facility capacity;
- customer orders and promised delivery;
- supplier-outage scenarios;
- constrained recovery planning;
- deterministic projections and evidence references.

## Explicitly outside the context

- full accounting and invoice settlement;
- detailed route, customs, and carrier optimization;
- supplier-contract negotiation;
- machine-level production and workforce scheduling;
- product returns;
- live ERP integration;
- autonomous execution;
- real-world forecasting beyond the defined scenario horizon.

## Modeling principles

- Operational records are facts or plans; projected results are derived states.
- Every quantity has a unit and every monetary amount has a currency.
- Time-dependent relationships are selected by effective interval.
- The model is deterministic for the same state, inputs, and rule version.
- Unsupported or missing information is surfaced instead of guessed.

## Boundary with later phases

Phase 2 defines meaning and rules. Phase 3 will create coherent data, Phase 4
will map the concepts to Db2, and later phases will implement impact,
simulation, and optimization behavior.
