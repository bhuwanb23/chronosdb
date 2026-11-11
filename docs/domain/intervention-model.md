# Phase 2N: Intervention Model

Every intervention has parameters, hard constraints, deterministic state
changes, feasibility status, and a machine-readable rejection reason.

## Do nothing

State change: none. It is the disrupted baseline against which every other
candidate is compared.

## Warehouse transfer

Parameters: source warehouse, destination warehouse, component, quantity,
transfer start, lead time, and cost.

Constraints:

- source inventory exists;
- quantity is positive and transferable;
- source safety stock and committed demand remain protected;
- destination is eligible;
- arrival is inside the horizon;
- material is not already allocated.

State changes: source balance decreases at dispatch, destination balance
increases at arrival, and transfer cost is added.

## Purchase-order expedition

Parameters: purchase order, new arrival time, and expedite cost.

Constraints: PO is outstanding and expedite-eligible, the new arrival precedes
the disrupted arrival, the outage does not make expedition impossible, and cost
is within budget.

Expedition cannot override a total supplier outage unless the model explicitly
supports an alternative logistics path or the order has already left the
supplier.

## Alternate supplier

Parameters: supplier, component, quantity, order time, lead time, and unit
price.

Constraints: approved effective agreement, minimum order, capacity, horizon,
and budget.

The incremental cost is the supplier premium relative to normal procurement;
the full replacement purchase cost is not counted as incremental twice.

## Production rescheduling

Parameters: production order, new priority/sequence, and rescheduling cost.

Constraints: order is not completed, in-progress work is not preempted,
facility capacity remains valid, and new customer impact is calculated.
Results must show both orders helped and orders harmed.

## Hybrid

The first supported hybrid is warehouse transfer plus alternate supplier. It is
one combined intervention and receives one simulation outcome; component
outcomes must not be added from separate independent runs.

## Statuses

`FEASIBLE`, `INFEASIBLE`, `INSUFFICIENT_DATA`, and `UNSUPPORTED` are distinct.
