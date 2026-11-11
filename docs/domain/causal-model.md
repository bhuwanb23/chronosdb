# Phase 2M: Causal Propagation Model

## Causal path

```text
Supplier outage
  -> affected outstanding purchase orders
  -> delayed component receipts
  -> lower projected component balance
  -> component shortage
  -> material unavailability
  -> delayed production start
  -> delayed production completion
  -> delayed product availability
  -> delayed customer delivery
  -> SLA breach
  -> revenue at risk
```

## Cause classes

- **Necessary operational constraint:** directly blocks an outcome, such as a
  missing mandatory component.
- **Contributing factor:** worsens an outcome without independently causing it,
  such as low safety stock.
- **Contextual evidence:** explains similarity or policy but does not establish
  current causality, such as a historical incident.

## Causal rules

- Every edge has a source, transformation, required data, output, failure
  state, and evidence reference.
- The model never jumps directly from supplier outage to revenue at risk.
- A derived customer result must retain all intermediate dependencies.
- Missing intermediate data produces an incomplete trace and
  `INSUFFICIENT_DATA`.
- A causal trace is valid only for its scenario, simulation run, state version,
  and rule version.

## Golden trace shape

```text
Supplier outage
  -> delayed purchase order
  -> delayed component receipt
  -> component shortage
  -> production delay
  -> customer delivery delay
  -> revenue at risk
```
