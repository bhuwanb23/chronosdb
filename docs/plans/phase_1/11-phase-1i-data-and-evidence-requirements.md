11. Phase 1I: Data and evidence requirements
Goal

Define what information Phase 2 and Phase 3 must model and generate.

11.1 Required operational data
Supplier data
Supplier ID
Supplier name
Status
Region
Reliability information, if used
Approved components
Normal lead time
Capacity
Effective dates
Component data
Component ID
Description
Unit of measure
Criticality
Safety stock
Substitution group
Unit cost
Product and BOM data
Product ID
Component ID
Required quantity
Scrap or yield factor, if used
Effective date
Mandatory or optional status
Inventory data
Warehouse
Component
On-hand quantity
Reserved quantity
Available quantity
Safety-stock requirement
Snapshot time
Purchase orders
Purchase-order ID
Supplier
Component
Quantity
Expected arrival
Status
Expedite eligibility
Unit cost
Production orders
Production-order ID
Product
Quantity
Facility
Planned start
Planned completion
Priority
Capacity requirement
Customer orders
Customer-order ID
Product
Quantity
Promised date
Revenue
SLA class
Priority
Assigned production order
Intervention information
Alternate supplier
Transfer lead time
Transfer cost
Expedite cost
Supplier premium
Production rescheduling limits
11.2 Required evidence documents
Supplier disruption notices
Historical incident reports
Approved substitution procedures
Inventory-transfer procedure
Shipment-expedition procedure
Customer SLA policy
Recovery approval policy
11.3 Data quality requirements

## The system must detect:

Missing foreign-key relationships
Negative quantities
Invalid date ordering
Duplicate active records
Expired substitutions
Unknown units
Conflicting inventory snapshots
Missing customer due date
Unsupported currencies
Unqualified alternate supplier
11.4 Evidence hierarchy

## Use:

## Level 1: Operational fact

Structured Db2 record.

## Examples:

Inventory quantity
Purchase-order arrival date
Production schedule
Customer due date
Level 2: Deterministic derived value

Calculated from structured facts.

## Examples:

Shortage date
Delay days
Revenue at risk
SLA status
Level 3: Controlled reference evidence

Retrieved procedure or historical incident.

## Examples:

Transfer procedure
Alternate-supplier policy
Similar historical outage
Level 4: Generated explanation

LLM-generated narrative constrained by Levels 1–3.

Level 4 must never override Levels 1–2.

Deliverable
docs/product/data-and-evidence-requirements.md

## Phase 2 dependency

## Phase 2 must translate these requirements into:

Entities
Relationships
Causal paths
Temporal semantics
Business rules
Units and constraints
