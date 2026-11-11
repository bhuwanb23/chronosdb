# Phase 2N: Feasibility Rule Catalogue

| Code | Rule |
|---|---|
| SOURCE_SAFETY_STOCK_VIOLATION | Transfer would reduce source below protected safety stock. |
| INSUFFICIENT_TRANSFERABLE_QUANTITY | Transfer quantity exceeds eligible source quantity. |
| SUPPLIER_NOT_APPROVED | Alternate supplier agreement is not approved and effective. |
| SUPPLIER_CAPACITY_EXCEEDED | Requested alternate quantity exceeds capacity. |
| MINIMUM_ORDER_NOT_MET | Alternate order is below the approved minimum. |
| RECOVERY_BUDGET_EXCEEDED | Incremental intervention cost exceeds budget. |
| PO_NOT_EXPEDITE_ELIGIBLE | Purchase order cannot be expedited. |
| OUTAGE_PREVENTS_EXPEDITION | Supplier outage makes the proposed expedition impossible. |
| ARRIVAL_OUTSIDE_HORIZON | Intervention arrival is after the simulation horizon. |
| PRODUCTION_ORDER_LOCKED | Production order is completed or locked in progress. |
| MISSING_REQUIRED_DATA | A required fact is absent or conflicting. |
| UNSUPPORTED_INTERVENTION | Intervention type is outside the current model. |

## Feasibility decision

Evaluate hard constraints before ranking. A candidate with any hard-constraint
failure is `INFEASIBLE`. A candidate lacking a required fact is
`INSUFFICIENT_DATA`, not infeasible. An unmodeled type is `UNSUPPORTED`.

The rejection code, input value, threshold, unit, and rule version must be
preserved for every non-feasible candidate.
