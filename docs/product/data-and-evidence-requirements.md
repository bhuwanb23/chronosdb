# Data and Evidence Requirements

This document defines information that Phase 2 and later data work must model.
It does not prescribe database tables.

## Operational data

### Supplier

Supplier ID, name, status, region, approved components, normal lead time,
capacity, and effective dates.

### Component

Component ID, description, unit of measure, criticality, safety stock,
substitution group, unit cost, and effective dates.

### Product and bill of materials

Product ID, component ID, required quantity, optional yield/scrap factor,
mandatory status, and effective date.

### Inventory

Warehouse, component, on-hand quantity, reserved quantity, available quantity,
safety-stock requirement, and snapshot time.

### Purchase order

Purchase-order ID, supplier, component, quantity, expected arrival, status,
expedite eligibility, and unit cost.

### Production order

Production-order ID, product, quantity, facility, planned start, planned
completion, priority, and capacity requirement.

### Customer order

Customer-order ID, product, quantity, promised date, revenue, SLA class,
priority, and assigned production order.

### Intervention inputs

Approved alternate supplier, transfer lead time, transfer cost, expedition
cost, supplier premium, and production-rescheduling limits.

## Evidence documents

The controlled evidence set may include:

- supplier disruption notices;
- historical incident reports;
- approved substitution procedures;
- inventory-transfer procedures;
- shipment-expedition procedures;
- customer SLA policy;
- recovery approval policy.

Each document requires source identity, version, effective dates, status,
access scope, and chunk identity when later indexed.

## Data-quality rules

The system must detect and report:

- missing relationships;
- negative quantities;
- invalid date ordering;
- duplicate active records;
- expired substitutions;
- unknown units or currencies;
- conflicting inventory snapshots;
- missing customer due dates;
- unqualified alternate suppliers.

Data-quality failures must become explicit warnings or
`INSUFFICIENT_DATA`; they must not be silently repaired.

## Evidence hierarchy

1. **Operational fact:** a structured Db2 record, such as inventory or due date.
2. **Deterministic derived value:** a documented calculation from operational
   facts, such as shortage date or revenue at risk.
3. **Controlled reference evidence:** an approved procedure or historical
   incident.
4. **Generated explanation:** a future narrative constrained by levels 1–3.

Level 4 may summarize levels 1–3 but can never override them.

## Phase 2 handoff

Phase 2 must translate these requirements into entities, relationships,
causal paths, temporal semantics, units, constraints, and business rules. It
must preserve explicit distinctions between facts, derived values, reference
evidence, and explanations.
