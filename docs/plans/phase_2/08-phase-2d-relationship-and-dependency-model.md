8. Phase 2D: Relationship and Dependency Model
Goal

Define cardinalities and dependency paths.

Core relationships
Plain Text
Supplier 1 ──< SupplierComponent >── 1 Component
 
Product 1 ──< BOMVersion 1 ──< BOMLine >── 1 Component
 
Warehouse 1 ──< InventorySnapshot >── 1 Component
 
Supplier 1 ──< PurchaseOrder >── 1 Component
 
Facility 1 ──< ProductionOrder >── 1 Product
 
ProductionOrder 1 ──< ProductionMaterialAllocation >── Component
 
CustomerOrder 1 ──< CustomerOrderLine >── Product
 
CustomerOrderLine 0..1 ── ProductionOrder
 
Scenario 1 ──< Intervention
 
Scenario 1 ──< SimulationRun
Intervention 1 ──< SimulationRun
Important cardinality decisions
Supplier and component
One supplier may supply many components.
One component may have many approved suppliers.
Approval is time-dependent.
Product and component
One product contains many BOM lines.
One component may appear in many products.
BOM version is selected based on operational time.
Production and customer orders

For MVP simplicity:

Each customer-order line may be associated with one production order.
One production order may fulfil multiple customer-order lines.
Partial fulfilment may occur.
Warehouse and facility

A production facility may consume from:

One default warehouse
Additional eligible warehouses through transfers

The default source and transfer eligibility must be explicit.

Dependency graph

The primary causal dependency is:

Plain Text
Supplier
→ Purchase order or expected replenishment
→ Component available quantity
→ Material allocation
→ Production order start/completion
→ Customer-order fulfilment
→ Delivery projection
→ SLA status
→ Revenue at risk
Deliverables
Plain Text
docs/domain/relationship-model.md
docs/domain/dependency-graph.md
Exit gate
Every causal edge corresponds to a documented relationship.
No hidden relationship is required for the golden scenario.
Cardinalities support alternate suppliers and multi-component products.
Customer impact can be traced back to supplier supply.
The graph is acyclic for the MVP calculation path.
