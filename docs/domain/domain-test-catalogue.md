# Phase 2T: Domain Test Catalogue

These are model-level tests for later implementation. They are not executable
tests yet.

## Entity tests

- `DT-ENT-001`: supplier-component agreement references existing entities.
- `DT-ENT-002`: inactive supplier cannot receive a new alternate order.
- `DT-ENT-003`: BOM line quantity is positive.
- `DT-ENT-004`: customer-order quantity is positive.

## Temporal tests

- `DT-TIME-001`: only the BOM active at production time is selected.
- `DT-TIME-002`: receipt cannot be consumed before arrival.
- `DT-TIME-003`: completed scenario excludes late-ingested data.
- `DT-TIME-004`: overlapping active agreements are rejected unless allowed.

## Inventory tests

- `DT-INV-001`: allocation cannot exceed eligible inventory.
- `DT-INV-002`: transfer cannot cross protected safety stock.
- `DT-INV-003`: quarantined inventory cannot be consumed.
- `DT-INV-004`: reservations are not subtracted twice.
- `DT-INV-005`: one inventory quantity cannot serve two allocations.

## BOM tests

- `DT-BOM-001`: requirement equals product quantity times BOM quantity.
- `DT-BOM-002`: scrap is applied exactly once.
- `DT-BOM-003`: missing active BOM returns `INSUFFICIENT_DATA`.
- `DT-BOM-004`: mandatory shortage blocks affected production.

## Production tests

- `DT-PRD-001`: production cannot begin before all materials are ready.
- `DT-PRD-002`: production cannot exceed facility capacity.
- `DT-PRD-003`: higher-priority orders are scheduled first.
- `DT-PRD-004`: tie-breaking is deterministic.
- `DT-PRD-005`: completed quantity is not rescheduled.

## Customer-impact tests

- `DT-CUS-001`: on-time delivery creates no revenue at risk.
- `DT-CUS-002`: partial lateness creates proportional revenue at risk.
- `DT-CUS-003`: missing promised date returns `INSUFFICIENT_DATA`.
- `DT-CUS-004`: multiple late lines count once at order level.

## Intervention tests

- `DT-INT-001`: unapproved alternate supplier is infeasible.
- `DT-INT-002`: budget-exceeding intervention is infeasible.
- `DT-INT-003`: expedition cannot bypass unsupported total outage.
- `DT-INT-004`: rescheduling calculates both helped and harmed orders.
- `DT-INT-005`: hybrid outcome is simulated jointly.

## Causal tests

- `DT-CAU-001`: every breached line has a complete causal path.
- `DT-CAU-002`: unaffected purchase order cannot appear in a disruption trace.
- `DT-CAU-003`: contextual document cannot create an operational fact.

## Golden benchmark assertions

- `DT-GOLD-001`: do-nothing breached orders equal 2.
- `DT-GOLD-002`: do-nothing revenue at risk equals INR 1,600,000.
- `DT-GOLD-003`: hybrid cost equals INR 132,000.
- `DT-GOLD-004`: hybrid breaches equal 0.
- `DT-GOLD-005`: hybrid revenue protected equals INR 1,600,000.
- `DT-GOLD-006`: recommendation equals `INT-HYBRID-400`.
