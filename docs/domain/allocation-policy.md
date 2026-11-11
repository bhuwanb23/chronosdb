# Phase 2I: Allocation Policy

## Reservation authority

The inventory snapshot stores physical on-hand, current reserved quantity, and
quarantined quantity. Future scenario allocation recalculates eligible demand
from the scenario state. The current reservation is not subtracted again from
the recalculated reservation.

The golden scenario must identify which reservations already exist at its
as-of time.

## Deterministic allocation order

When eligible material is scarce, allocate in this order:

1. already in-progress production orders;
2. released production orders;
3. higher-priority customer commitments;
4. earlier promised delivery;
5. earlier production-order creation time;
6. stable production-order identifier.

The same ordering applies on every run with the same rule version.

## Eligibility

An allocation is eligible only when:

- the component matches the active BOM requirement;
- the inventory is available at or before consumption time;
- the warehouse is eligible for the facility;
- the quantity has not already been allocated;
- unit and time constraints are compatible.

## Allocation outcomes

- `ALLOCATED`: the full required quantity is assigned.
- `PARTIALLY_ALLOCATED`: only part is assigned.
- `UNALLOCATED`: no eligible quantity is assigned.
- `INSUFFICIENT_DATA`: a required source fact is absent or conflicting.

Partial allocation contributes to late or delayed quantity according to the
production and customer rules. It is not silently rounded to full allocation.

## Transfer policy

Transfers are optional interventions, not implicit allocations. A transfer
must identify source, destination, component, quantity, dispatch time, arrival
time, and cost. The source safety-stock and committed-demand checks occur
before the transfer is considered feasible.
