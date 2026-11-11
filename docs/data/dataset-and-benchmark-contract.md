# Phase 3B: Dataset and Benchmark Contract

## Dataset layers

1. **Master**: locations, facilities, warehouses, lanes, suppliers,
   components, products, BOMs, customers, and policies.
2. **Operational history**: receipts, inventory snapshots, purchase orders,
   production orders, customer orders, and disruptions.
3. **Scenario overlays**: immutable baseline plus isolated disruption and
   intervention overlays.
4. **Ground truth**: calculated impacts, feasibility, costs, provenance, and
   recommendations.
5. **Evidence**: source records, rule/formula IDs, versions, and run metadata.

Master records are generated in Phase 3G. Operational and scenario layers are
reserved for later Phase 3 work and must not be inferred by the master
generator.

## Dataset objectives

- Every record is referentially valid and semantically typed.
- Same seed and configuration produce byte-identical canonical exports.
- Independent seed streams prevent changes in one layer from perturbing others.
- Records cover normal, impacted, infeasible, insufficient-data, partial
  fulfilment, and no-impact cases in later benchmark phases.
- Every numerical ground-truth output has formula, unit, reference case, and
  provenance metadata.

## Benchmark partitions

| Partition | Purpose | May contain labels? |
|---|---|---|
| `train` | Development and generator checks | Yes |
| `validation` | Rule/model tuning | Yes, held out from tuning | 
| `test` | Final measurement | Labels withheld from consumers |
| `golden` | Frozen Phase 2 scenario regression | Yes, immutable |
| `adversarial` | Falsification and invariant checks | Yes |

The golden and adversarial partitions are not sampled from ordinary records.
They are named fixtures with frozen expected outputs.

## Leakage controls

- Split by scenario family and temporal episode, never by individual rows.
- Do not copy a customer, supplier, order, or scenario ID across train and
  evaluation partitions unless it is an explicitly shared master key.
- Do not place projected outcomes, recommendation fields, or future receipts in
  predictive input records.
- Store `as_of_time` and `event_time`; validation rejects input whose event time
  is later than the scenario as-of time.
- Keep benchmark labels in separate files and manifests.
- Use independent benchmark and generation streams.
- Canonical hashes and manifest versions make accidental regeneration visible.

## Contract gate

Master-data exports must satisfy identifier, relationship, unit, currency,
effective-date, positivity, and reproducibility checks before they are input
to operational-data generation.
