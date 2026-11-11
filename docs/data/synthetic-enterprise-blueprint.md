# Phase 3C: Synthetic Enterprise Blueprint

## Enterprise

**Asterion Control Systems** is a synthetic industrial-electronics manufacturer.
Its planning currency is INR, quantities use `EA`, timestamps are stored in UTC,
and user-facing examples use Asia/Kolkata.

The network contains Pune and Chennai operations, two manufacturing facilities,
three warehouses, approved primary and alternate suppliers, components,
finished products, customers, and versioned BOMs.

## Master-data rules

- Every supplier supplies at least one component through a dated agreement.
- Every component belongs to at least one product BOM.
- Every product has one active BOM at the dataset reference time.
- BOM quantities and capacities are strictly positive.
- Supplier approvals and agreement intervals are explicit.
- Customers have a default SLA policy; orders may override it later.
- IDs are stable within a semantic dataset version.

## Golden compatibility

The Phase 2 golden fixture remains an alias-compatible example:
`S-104`, `S-208`, `C-MCU-42`, `P-CONTROLLER-X`, `PO-2208`, `PROD-876`,
and `CO-701`. Generated Phase 3 master IDs use the same entity-family
semantics (`SUP-`, `CMP-`, `PRD-`, etc.) and must not redefine those golden
records as a second identity.
