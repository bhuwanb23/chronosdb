# Phase 2D: Relationship Model

## Core cardinalities

```text
Supplier 1 ──< SupplierComponentAgreement >── 1 Component
Product 1 ──< BOMVersion 1 ──< BOMLine >── 1 Component
Warehouse 1 ──< InventorySnapshot >── 1 Component
Supplier 1 ──< PurchaseOrder >── 1 Component
Facility 1 ──< ProductionOrder >── 1 Product
ProductionOrder 1 ──< MaterialAllocation >── 1 Component
CustomerOrder 1 ──< CustomerOrderLine >── 1 Product
CustomerOrderLine 0..1 ── ProductionOrder
Scenario 1 ──< Intervention
Scenario 1 ──< SimulationRun
Intervention 1 ──< SimulationRun
Scenario 1 ──< DecisionResult
```

## Decisions

### Supplier and component

One supplier may supply many components and one component may have many
supplier agreements. Approval and supply terms are effective-dated.

### Product and component

One product may have many BOM lines and one component may appear in many
products. The BOM version active at the relevant operational time is selected;
the latest version is not a valid fallback.

### Inventory and production

A production facility has one default warehouse for the MVP and may receive
additional material through explicit eligible transfers. Material allocation
identifies both the component and source warehouse.

### Production and customer orders

Each customer-order line may be associated with at most one production order.
One production order may fulfil multiple customer-order lines, including
partial fulfilment.

### Scenarios and outcomes

A scenario is immutable after freeze. It can have many interventions and
simulation runs. A simulation run references exactly one scenario and one
intervention, including the do-nothing intervention. A decision result selects
at most one intervention for human review.

## Relationship rules

- An inactive or expired supplier agreement cannot support a new intervention.
- A customer line cannot reference a production order for a different product.
- A material allocation must reference a component required by the selected BOM.
- An inventory snapshot must identify one warehouse, component, and snapshot time.
- A simulation cannot create a relationship that does not exist in its scenario
  overlay.
