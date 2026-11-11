# Phase 2C: Conceptual Entity and Value-Object Model

This is a conceptual model. Names and attributes define business meaning; they
are not a physical Db2 schema.

## Entity catalogue

| Entity | Stable ID | Key attributes |
|---|---|---|
| Supplier | `supplier_id` | name, status, region, effective interval |
| Supplier component agreement | `supplier_component_id` | supplier, component, approval, lead time, limits, capacity, price, effective interval |
| Component | `component_id` | name, unit, criticality, cost, currency, substitution group, status |
| Product | `product_id` | name, unit, standard revenue, currency, status |
| BOM version | `bom_version_id` | product, version, effective interval, status |
| BOM line | `bom_line_id` | BOM version, component, quantity, scrap factor, mandatory |
| Warehouse | `warehouse_id` | name, region, status |
| Facility | `facility_id` | name, region, status, daily capacity |
| Inventory snapshot | `inventory_snapshot_id` | warehouse, component, time, on-hand, reserved, quarantined |
| Purchase order | `purchase_order_id` | supplier, component, destination, ordered/received quantity, arrival, status, cost, expedite eligibility |
| Production order | `production_order_id` | product, facility, planned/completed quantity, start/completion, priority, status |
| Material allocation | `allocation_id` | production order, component, warehouse, required/allocated quantity, status |
| Customer order | `customer_order_id` | customer, order time, promised time, priority, SLA class, status |
| Customer-order line | `customer_order_line_id` | order, product, ordered/allocated quantity, unit revenue, production order |
| Disruption event | `disruption_event_id` | type, supplier, start/end, reported time, status, scope |
| Scenario | `scenario_id` | as-of time, disruption, objective, constraints, created time, rule version, status |
| Intervention | `intervention_id` | scenario, type, parameters, status |
| Simulation run | `simulation_run_id` | scenario, intervention, input-state version, rule version, times, status |
| Decision result | `decision_result_id` | scenario, selected intervention, objective, score, creation time, review status |

## Ownership boundaries

- Supplier agreements own approval and supply terms, not current inventory.
- Warehouses own component stock; facilities consume material through
  allocations.
- BOM versions own product composition for an effective interval.
- Scenarios own immutable hypothetical inputs, not live operational facts.
- Simulation runs own derived outcomes for one scenario/intervention pair.
- Decision results own selection and review status, not execution of actions.

## Value objects

| Value object | Required fields | Rule |
|---|---|---|
| Quantity | value, unit | Unit is mandatory and compatible with the component. |
| Money | amount, currency | Different currencies cannot be combined implicitly. |
| Effective interval | valid-from, valid-to | Half-open interval; end is exclusive. |
| Lead time | duration, time basis | MVP uses elapsed calendar time. |
| Cost constraint | amount, currency | Must be non-negative. |
| Service target | threshold, unit | Unit is explicit, such as breach count or service ratio. |
| Optimization weights | objective, weights | Objective and weights are visible. |
| Inventory position | on-hand, reserved, quarantined | Derived availability is traceable. |
| Shortage result | component, time, required, allocatable, shortage | Derived and rule-versioned. |
| Delay result | order, committed time, projected time, delay | Derived and time-zone aware. |
| Evidence reference | source type, source ID, version | Must point to an existing source. |

## Invariants

Every entity has a stable identifier. Many-to-many relationships are represented
by an explicit concept. Versioned concepts have effective intervals. Quantities
and money cannot be unitless.
