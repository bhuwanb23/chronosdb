15. Phase 5K: Production Scheduling Engine
Goal

Convert material availability and facility capacity into projected manufacturing timelines.

Scheduling model

For each production batch:

ProjectedStart=max⁡(PlannedStart,MaterialReadyTime,CapacityReadyTime)ProjectedStart = \max( PlannedStart, MaterialReadyTime, CapacityReadyTime )ProjectedStart=max(PlannedStart,MaterialReadyTime,CapacityReadyTime) ProjectedCompletion=ProjectedStart+ProcessingDurationProjectedCompletion = ProjectedStart + ProcessingDurationProjectedCompletion=ProjectedStart+ProcessingDuration ProductionDelay=max⁡(0,ProjectedCompletion−PlannedCompletion)ProductionDelay = \max( 0, ProjectedCompletion - PlannedCompletion )ProductionDelay=max(0,ProjectedCompletion−PlannedCompletion)
Batch model

Golden scenario:

Plain Text
Batch size: 100 finished units
Capacity use: 100 finished units per calendar day
Material issue: batch start
Duration: 24 hours for one 100-unit batch
Scheduling queue

Order batches by:

Already in progress
Released status
Explicit production priority
Highest linked customer priority
Earliest promised date
Planned start
Stable order and batch ID
Facility capacity

For each time bucket:

AllocatedCapacityt≤EffectiveCapacitytAllocatedCapacity_t \le EffectiveCapacity_tAllocatedCapacityt​≤EffectiveCapacityt​

A production batch may not overlap unavailable capacity unless partial-capacity processing is explicitly supported.

No artificial deadlock

Because material availability depends on production allocation and scheduling, implement a clear sequence:

Load fixed in-progress commitments.
Build candidate order queue.
For each batch in priority order:
Determine earliest material-ready time.
Determine earliest capacity-ready time.
Select projected start.
Consume material at projected start.
Reserve capacity.
Calculate completion.
Continue until horizon end.
Projected production result
JSON
{
"production_order_id": "MO-0882",
"planned_start": "...",
"planned_completion": "...",
"projected_start": "...",
"projected_completion": "...",
"delay_hours": 288,
"blocking_components": ["CMP-MCU-42"],
"blocking_receipts": ["PO-2208"],
"batches": []
}
Horizon behavior

If material or capacity does not become available:

Plain Text
projected_start: null
projected_completion: null
status: NOT_COMPLETED_WITHIN_HORIZON

Do not invent a completion date beyond available information unless the event schedule supports it.

Deliverables
Plain Text
src/backend/chronosdb/impact/production/
docs/impact-engine/production-scheduling.md
Acceptance criteria
Golden scheduling timeline matches the frozen expected timeline.
Facility capacity is never exceeded.
Material is consumed exactly once.
Stable tie-breaking produces repeatable schedules.
Delaying one order can correctly affect later orders.

