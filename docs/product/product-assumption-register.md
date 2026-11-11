# Product Assumption Register

| ID | Assumption | Risk if false | Owner/phase |
|---|---|---|---|
| A-001 | One supplier may supply multiple components. | Dependency model is incomplete. | Phase 2 |
| A-002 | A component may have multiple approved suppliers. | Alternate-supply scenarios are invalid. | Phase 2 |
| A-003 | Products may require multiple components. | Impact cascade is understated. | Phase 2 |
| A-004 | Required component availability constrains production. | Delay calculation is unreliable. | Phase 2 |
| A-005 | Customer orders map to products and delivery commitments. | SLA impact cannot be derived. | Phase 2 |
| A-006 | Revenue at risk means value of projected SLA-breaching orders, not confirmed loss. | Financial output is misleading. | Phase 2 |
| A-007 | MVP cost and revenue use one normalized currency. | Candidate comparison is invalid. | Phase 2 |
| A-008 | Transfer feasibility can initially use lead time, cost, and safety stock. | Logistics model is oversimplified. | Phase 2 |
| A-009 | The MVP uses labelled synthetic data. | Results could be mistaken for production evidence. | Phase 3 |
| A-010 | Interventions require human approval. | System could be misused as an execution tool. | Product |
| A-011 | The baseline is immutable for every candidate simulation. | Comparisons are not reproducible. | Phase 6 |

Each assumption must be confirmed, rejected, or revised before the dependent
implementation is marked complete.
