# Material Requirements and Allocation

Requirements are calculated per production batch from the BOM active at the
planned production start:

`required = ceil(batch_quantity * quantity_per * (1 + scrap_factor))`

Allocation is stable and single-use. Locked or earlier production obligations
are considered first, followed by customer priority, required time, order ID,
batch ID, and component ID. Opening inventory and projected receipts are
represented as source lots, so every allocation can identify its source.

Reservations reduce unreserved availability only once. A future receipt can
make a requirement material-ready without being incorrectly consumed before
its arrival.
