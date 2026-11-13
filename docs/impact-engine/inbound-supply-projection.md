# Inbound-Supply Projection

Only the outstanding quantity of an affected purchase order becomes a
`PROJECTED_PURCHASE_RECEIPT`. Historical receipts remain facts, the source
purchase order is not mutated, and the original future receipt is not emitted
a second time.

Projected receipts beyond the simulation horizon are retained with
`within_horizon: false`; they are unresolved future supply and are excluded
from within-horizon availability calculations.
