# Phase 2D: Dependency Graph

## Primary causal path

```text
Supplier
  -> Supplier component agreement
  -> Purchase order or expected replenishment
  -> Component availability
  -> Material allocation
  -> Production order start/completion
  -> Customer-order fulfilment
  -> Delivery projection
  -> SLA status
  -> Revenue at risk
```

## Edge meaning

| Edge | Meaning |
|---|---|
| Supplier → supply | An approved supplier agreement makes replenishment possible. |
| Supply → component availability | Receipts change projected component balance at arrival. |
| Availability → material allocation | Eligible material is allocated by the allocation policy. |
| Allocation → production | A mandatory component can constrain start or completion. |
| Production → fulfilment | Projected production completion constrains customer delivery. |
| Fulfilment → SLA | Projected delivery is compared with the commitment rule. |
| SLA → revenue at risk | Late or unfulfilled quantity is valued by the financial rule. |

## Graph constraints

- The MVP calculation path is acyclic.
- Every edge must be supported by a conceptual relationship and rule.
- A supplier outage may affect expected supply but does not undo received
  quantity or completed production.
- Evidence must permit traversal from a derived customer impact back to the
  originating supplier and source records.
- Unmodeled cross-domain effects are marked `INSUFFICIENT_DATA`, not inferred.

## Later-phase boundary

This graph is a causal specification, not an execution algorithm. Inventory
allocation, BOM requirements, production scheduling, SLA rules, intervention
overlays, and formulas are defined in later Phase 2 sections.
