# Production Scheduling

Production is scheduled as deterministic batches. For each batch:

`projected_start = max(planned_start, material_ready_time, capacity_ready_time)`

The default golden policy uses 100 finished units and 24 hours per batch.
Facility capacity is reserved by calendar date and cannot be exceeded.
Material is consumed at the projected start exactly once.

If material or capacity cannot become available before the horizon, projected
start and completion remain null and the batch is marked
`NOT_COMPLETED_WITHIN_HORIZON`.
