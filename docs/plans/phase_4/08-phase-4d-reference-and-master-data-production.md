8. Phase 4D: Reference and Master-Data Production
Goal

Generate the stable enterprise entities upon which all operational records depend.

8.1 Warehouses
Required records
Plain Text
WH-PUNE
WH-CHENNAI
WH-GURUGRAM

Each warehouse must define:

Region
Timezone
Operating status
Effective interval
Supported facilities
Transfer eligibility
Component-storage eligibility
8.2 Facilities
Plain Text
FAC-PUNE
FAC-CHENNAI

Each facility defines:

Daily production capacity
Supported product families
Operating calendar
Source warehouse
Effective interval
Status
8.3 Suppliers

Twenty-four synthetic suppliers must show a meaningful availability mix:

Primary suppliers
Alternate approved suppliers
Conditional suppliers
Inactive historical suppliers
Example classes
Plain Text
DOMESTIC_REGIONAL
DOMESTIC_NATIONAL
ASIA_IMPORT
EUROPE_IMPORT

These classifications control configured lead-time ranges only.

8.4 Components

The component population must include:

Critical single-source components
Dual-source components
Widely available components
High-value and low-value materials
Components with alternate suppliers
Components without valid alternatives
Components with expired alternatives
8.5 Products and BOMs

Every active product must have:

Exactly one active BOM at a given time
At least three BOM lines
At least one operationally important component
A valid effective interval
No cyclic dependency
8.6 Customers and SLA policies

Each synthetic customer must map to:

Strategic, Enterprise, or Standard class
One active SLA policy
Priority rules
Delivery lead-time rule
Validation targets
Metric	Target
Duplicate IDs	0
Orphan master references	0
Products without active BOM	0
Overlapping active BOMs	0
Active components without supply path	0, unless intentionally flagged
Invalid effective intervals	0
Invalid units	0
Deliverables
Plain Text
data/releases/v1.0.0/master/
├── warehouses.csv
├── facilities.csv
├── facility_product_capabilities.csv
├── warehouse_facility_links.csv
├── transfer_lanes.csv
├── suppliers.csv
├── components.csv
├── supplier_component_agreements.csv
├── products.csv
├── bom_versions.csv
├── bom_lines.csv
├── customers.csv
└── sla_policies.csv
