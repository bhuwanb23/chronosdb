# Phase 2 Question Register

Phase 2 must answer these questions before schema and simulator work is
considered complete.

## Domain questions

- **DOM-001:** Which entities define the operational supply-chain state?
- **DOM-002:** Can one component substitute for another, and under which rules?
- **DOM-003:** How are bill-of-material effective dates represented?
- **DOM-004:** How is reserved inventory allocated across orders?
- **DOM-005:** What exact condition delays a production order?
- **DOM-006:** How is customer delivery derived from production completion?

## Temporal questions

- **TIME-001:** Which timestamp defines the state used by a scenario?
- **TIME-002:** How are late-arriving updates handled?
- **TIME-003:** Are snapshots daily, hourly, or event-based?
- **TIME-004:** What happens when validity intervals overlap?
- **TIME-005:** Which timestamps are event time, effective time, and ingestion time?

## Financial and unit questions

- **FIN-001:** Which components make up recovery cost?
- **FIN-002:** Is revenue at risk full order value or a partial value for delayed
  orders?
- **FIN-003:** Which currency and exchange-rate rule applies?
- **FIN-004:** Which units are valid for quantity, time, capacity, and cost?

## Constraint and optimization questions

- **OPT-001:** Which constraints are hard and which are preferences?
- **OPT-002:** How are objectives normalized into comparable scores?
- **OPT-003:** How are ties and Pareto-equivalent candidates handled?
- **OPT-004:** Can a hybrid intervention be partially applied?
- **OPT-005:** How are supplier capacity and facility capacity consumed?

## Evidence questions

- **EVD-001:** Which operational records are authoritative when sources conflict?
- **EVD-002:** How are document versions and access scope enforced?
- **EVD-003:** What minimum source rows are required for each major claim?
- **EVD-004:** Which historical incidents are relevant evidence rather than
  current-state facts?

Each question needs a decision, owner, affected requirement, and test impact in
the Phase 2 domain and causal model.
