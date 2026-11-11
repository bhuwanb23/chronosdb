11. Phase 3G: Master-Data Generation
Goal

Generate structurally coherent domain master data.

11.1 Locations

Generate:

Regions
Warehouses
Facilities
Allowed warehouse-to-facility relationships
Transfer lanes

Each transfer lane needs:

Plain Text
source_warehouse
destination_warehouse
lead_time_hours
fixed_cost
variable_cost_per_unit
active_from
active_to
11.2 Suppliers

Generate:

Stable identifiers
Synthetic names
Regions
Active status
Effective dates

Avoid real company names.

Example synthetic names:

NovaCircuit Components
Meridian Micro Systems
Vardhan Industrial Electronics
BlueArc Sensor Works
11.3 Components

Ensure:

Unique ID
Canonical unit
Criticality
Standard unit cost
Safety-stock policy
Optional substitution group
11.4 Supplier-component agreements

Enforce:

Effective approval
Unique active relationship per supplier and component
Positive price
Positive lead time
Capacity
Minimum-order constraint
Currency consistency
11.5 Products and BOMs

Ensure:

Every active product has one active BOM at any time.
Every BOM has at least one line.
Every BOM line references an active component.
Quantity is positive.
No duplicate component line exists within one BOM.
Effective intervals do not overlap.
11.6 Customers and SLAs

Generate synthetic customers with:

Customer class
SLA class
Delivery lead-time rule
Priority
Effective intervals
Deliverables
Plain Text
data/generated/master/
├── suppliers.csv
├── components.csv
├── supplier_component_agreements.csv
├── products.csv
├── bom_versions.csv
├── bom_lines.csv
├── warehouses.csv
├── facilities.csv
├── transfer_lanes.csv
├── customers.csv
└── sla_policies.csv
Master-data invariants
Orphan references: 0
Duplicate primary IDs: 0
Invalid units: 0
Invalid currencies: 0
Overlapping active BOM versions: 0
Products without active BOM: 0
Active components without any valid supply path: allowed only when deliberately labelled as a benchmark condition
