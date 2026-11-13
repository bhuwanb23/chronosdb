# Customer Fulfilment

Completed production batches create product-availability events. Customer
lines receive stable, bounded fulfilment segments in customer priority order.
The sum of segment quantities never exceeds the open line quantity.

Projected delivery is calculated from availability and the configured delivery
lead-time policy. Partial fulfilment remains visible as separate segments
rather than being collapsed into a misleading single status.
