# Phase 16I: Data Dictionary

## Phase 16 Deep Dive: Documentation and Architecture Package

### Document every core entity.

### Required Entries

#### SUPPLIER
- **Description:** Supplier entity in ChronosDB
- **Keys:** supplier_id, name, region, status
- **Relationships:** Components, Orders
- **Business Meaning:** Source of components and materials

#### COMPONENT
- **Description:** Component entity in ChronosDB
- **Keys:** component_id, name, supplier_id, type
- **Relationships:** Suppliers, Inventory, Orders
- **Business Meaning:** Parts used in production

#### WAREHOUSE
- **Description:** Warehouse entity in ChronosDB
- **Keys:** warehouse_id, location, capacity
- **Relationships:** Inventory, Orders
- **Business Meaning:** Storage location

#### PURCHASE_ORDER
- **Description:** Purchase order entity in ChronosDB
- **Keys:** order_id, supplier_id, component_id, quantity, status
- **Relationships:** Suppliers, Components, Inventory
- **Business Meaning:** Order for components

#### PRODUCTION_ORDER
- **Description:** Production order entity in ChronosDB
- **Keys:** order_id, component_id, quantity, status
- **Relationships:** Components, Inventory, Orders
- **Business Meaning:** Production order

#### CUSTOMER_ORDER
- **Description:** Customer order entity in ChronosDB
- **Keys:** order_id, product_id, quantity, status
- **Relationships:** Products, Inventory, Orders
- **Business Meaning:** Customer order

#### SCENARIO
- **Description:** Scenario entity in ChronosDB
- **Keys:** scenario_id, type, status
- **Relationships:** Impact, Simulation, Optimization, Evidence, Narration, Audit
- **Business Meaning:** Operational scenario

#### SIMULATION
- **Description:** Simulation entity in ChronosDB
- **Keys:** simulation_id, scenario_id, result
- **Relationships:** Scenario, Optimization, Evidence
- **Business Meaning:** Counterfactual future

#### DECISION
- **Description:** Decision entity in ChronosDB
- **Keys:** decision_id, scenario_id, recommendation, evidence
- **Relationships:** Scenario, Optimization, Evidence, Audit
- **Business Meaning:** Recommended action

### Deliverable Location
`/home/user/chronosdb/docs/data-dictionary.md`

## Phase 16I Status: ✅ COMPLETE
