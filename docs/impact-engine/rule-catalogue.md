# Impact Rule Catalogue

Rule set: `impact-rules-v1.0.0`  
Domain model: `phase4-domain-model-1.0.0`  
Dataset compatibility: `1.0.0`

| Rule | Name | Inputs | Outputs | Rounding |
|------|------|--------|---------|----------|
| STATE-001 | effective state selection | effective interval, as-of time | eligible record | none |
| STATE-002 | information-time selection | ingested time, as-of time | known record | none |
| SUP-001 | outstanding quantity | ordered, received | outstanding quantity | decimal(3) |
| SUP-004 | disrupted arrival | original arrival, outage end, recovery lag | disrupted arrival, delay | none |
| SUP-005 | affected purchase order | supplier, outstanding, scope | affected flag | none |
| SUP-006 | projected receipt quantity | outstanding quantity | receipt quantity | decimal(3) |
| INV-003 | component shortage | requirement, allocation, required time | shortage quantity/type | decimal(3) |
| INV-004 | projected inventory balance | opening, receipts, consumption, transfers | projected balance | decimal(3) |
| ALLOC-001 | material allocation | requirement, source lots, priority | allocated quantity/lots | decimal(3) |
| PROD-003 | projected production schedule | planned start, material/capacity readiness | start, completion, delay | none |
| FUL-001 | customer fulfilment | open quantity, availability, lead time | segments, late quantity | decimal(3) |
| SLA-001 | SLA classification | projected and promised delivery | status, delay hours | none |
| FIN-004 | revenue at risk | late quantity, unit revenue | revenue, currency | decimal(2) |
| CAU-001 | causal trace | disruption, affected records, impacts | nodes, edges, attribution | none |
| DQ-001 | state completeness | required and loaded record classes | data quality status | none |

Every computed output references one of these rule IDs. The authoritative
definitions, including formulas and failure conditions, live in
`config/rules/impact-rules-v1.0.0.yaml`.
