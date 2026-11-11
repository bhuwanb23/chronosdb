# Phase 3A: Phase 2 Handoff Review

## Handoff status

The Phase 2 domain package under `docs/domain/` is the authority for dataset
meaning and validation.

| Input | Dataset interpretation | Status |
|---|---|---|
| Entities and relationships | Master-data and future transaction records | Confirmed |
| Lifecycles | Valid status and transition values | Confirmed |
| Units and finance | EA golden quantities, INR, explicit precision | Confirmed |
| Temporal model | UTC storage, Asia/Kolkata display, effective intervals | Confirmed |
| Supplier outage | Scenario event with configurable recovery lag | Confirmed |
| Inventory/allocation | Derived balances and deterministic priority | Confirmed |
| BOM/production/SLA | Ground-truth calculation inputs | Confirmed |
| Intervention/counterfactual | Scenario and expected-outcome layers | Confirmed |
| Provenance/data quality | Source, rule, version, and completeness metadata | Confirmed |
| Golden scenario | Corrected 400-unit-transfer fixture | Confirmed |

## Frozen generation decisions

- Partial production is allowed in 100-finished-unit batches.
- Partial customer delivery is allowed.
- Facility capacity is shared across products.
- Materials are consumed at batch start.
- Customer allocation order is priority, promised date, then stable ID.
- Time resolution is one hour; planning uses calendar time.
- Primary currency is INR.
- The golden component unit is EA.

## Questions resolved for dataset generation

- Outstanding PO quantity is `max(ordered - received, 0)`.
- Incremental costs are premiums/fees/transfer/rescheduling costs, not repeated
  base purchase cost.
- Ties use stable identifiers after the documented objective tie sequence.
- Transfer feasibility protects source safety stock and committed demand.

## Gate result

**Pass.** Dataset generation can begin without inventing domain semantics.
