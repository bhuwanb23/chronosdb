# ChronosDB Phase 2A–2G Domain Contract

This folder contains the conceptual domain model required before data
generation and physical Db2 design.

## Artifacts

### Handoff and context

- [`phase-1-handoff-review.md`](phase-1-handoff-review.md)
- [`bounded-context.md`](bounded-context.md)
- [`domain-glossary.md`](domain-glossary.md)

### Entities and relationships

- [`conceptual-entity-model.md`](conceptual-entity-model.md)
- [`relationship-model.md`](relationship-model.md)
- [`dependency-graph.md`](dependency-graph.md)

### Lifecycle and financial semantics

- [`state-transition-model.md`](state-transition-model.md)
- [`units-and-financial-model.md`](units-and-financial-model.md)

### Temporal semantics

- [`temporal-model.md`](temporal-model.md)
- [`time-examples.md`](time-examples.md)

- [`phase-2a-g-completion-report.md`](phase-2a-g-completion-report.md)

## Locked A–G decisions

- The bounded context is simplified manufacturing supply-chain planning.
- The primary causal path runs from supplier supply through component,
  production, customer delivery, SLA, and revenue at risk.
- Baseline and do-nothing are distinct.
- Quantities have units; money uses INR in the MVP.
- Effective intervals are half-open and canonical time is UTC.
- Historical state uses records valid and known at scenario as-of time.
- A–G is conceptual; later Phase 2 sections define disruption, inventory,
  BOM, scheduling, SLA, intervention, counterfactual, provenance, uncertainty,
  golden scenario, and benchmarks.
