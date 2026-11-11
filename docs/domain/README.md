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

### Disruption and inventory — Phase 2H–2I

- [`disruption-model.md`](disruption-model.md)
- [`inventory-model.md`](inventory-model.md)
- [`allocation-policy.md`](allocation-policy.md)

### Material, production, and customer impact — Phase 2J–2L

- [`bom-model.md`](bom-model.md)
- [`material-requirement-formulas.md`](material-requirement-formulas.md)
- [`production-scheduling-model.md`](production-scheduling-model.md)
- [`production-priority-policy.md`](production-priority-policy.md)
- [`customer-fulfilment-model.md`](customer-fulfilment-model.md)
- [`sla-and-revenue-model.md`](sla-and-revenue-model.md)

### Causality and counterfactuals — Phase 2M–2O

- [`causal-model.md`](causal-model.md)
- [`causal-edge-catalogue.md`](causal-edge-catalogue.md)
- [`causal-trace-format.md`](causal-trace-format.md)
- [`intervention-model.md`](intervention-model.md)
- [`feasibility-rule-catalogue.md`](feasibility-rule-catalogue.md)
- [`counterfactual-model.md`](counterfactual-model.md)

### Formulas, evidence, and uncertainty — Phase 2P–2R

- [`formula-catalogue.md`](formula-catalogue.md)
- [`objective-and-ranking-model.md`](objective-and-ranking-model.md)
- [`provenance-model.md`](provenance-model.md)
- [`uncertainty-and-data-quality-model.md`](uncertainty-and-data-quality-model.md)

### Golden scenario — Phase 2S

- [`golden-scenario/scenario-definition.md`](golden-scenario/scenario-definition.md)
- [`golden-scenario/input-records.csv`](golden-scenario/input-records.csv)
- [`golden-scenario/manual-calculation.md`](golden-scenario/manual-calculation.md)
- [`golden-scenario/do-nothing-result.json`](golden-scenario/do-nothing-result.json)
- [`golden-scenario/intervention-results.json`](golden-scenario/intervention-results.json)
- [`golden-scenario/expected-recommendation.json`](golden-scenario/expected-recommendation.json)
- [`golden-scenario/causal-traces.md`](golden-scenario/causal-traces.md)
- [`golden-scenario/assumptions.md`](golden-scenario/assumptions.md)

### Tests, review, and handoff — Phase 2T–2V

- [`domain-test-catalogue.md`](domain-test-catalogue.md)
- [`domain-review-report.md`](domain-review-report.md)
- [`adversarial-scenarios.md`](adversarial-scenarios.md)
- [`invariant-catalogue.md`](invariant-catalogue.md)
- [`phase-2-traceability-matrix.csv`](phase-2-traceability-matrix.csv)
- [`phase-2-completion-report.md`](phase-2-completion-report.md)

- [`phase-2a-g-completion-report.md`](phase-2a-g-completion-report.md)
- [`phase-2h-o-completion-report.md`](phase-2h-o-completion-report.md)

## Locked A–G decisions

- The bounded context is simplified manufacturing supply-chain planning.
- The primary causal path runs from supplier supply through component,
  production, customer delivery, SLA, and revenue at risk.
- Baseline and do-nothing are distinct.
- Quantities have units; money uses INR in the MVP.
- Effective intervals are half-open and canonical time is UTC.
- Historical state uses records valid and known at scenario as-of time.
- Disruption, inventory, BOM, scheduling, SLA, intervention, and counterfactual
  rules are conceptual and deterministic.
- P–V is complete as a specification and manually validated ground-truth
  package; executable implementation remains in later phases.
