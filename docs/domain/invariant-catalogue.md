# Phase 2U: Invariant Catalogue

| ID | Invariant |
|---|---|
| INV-001 | Ending inventory equals starting inventory plus receipts and transfers in minus consumption and transfers out. |
| INV-002 | Physical on-hand quantity is never negative. |
| INV-003 | Allocated quantity is no greater than eligible available quantity. |
| INV-004 | Transfer quantity is no greater than transferable quantity. |
| INV-005 | The same inventory cannot be allocated to multiple orders. |
| INV-006 | Reserved inventory is not subtracted twice. |
| INV-007 | Completed quantity is no greater than planned quantity. |
| INV-008 | Projected completion is no earlier than projected start. |
| INV-009 | Projected delivery is no earlier than product availability. |
| INV-010 | Revenue at risk is between zero and total open-order revenue. |
| INV-011 | Intervention cost is non-negative. |
| INV-012 | Missing data is not represented as zero. |
| INV-013 | Operational state is immutable during counterfactual evaluation. |
| INV-014 | Candidate overlays cannot read or mutate another candidate overlay. |
| INV-015 | Every business-impact output has a complete causal path or an explicit incomplete status. |
| INV-016 | Every displayed delta names its reference case. |

Any invariant violation is a model or data-quality failure and blocks the
affected result.
