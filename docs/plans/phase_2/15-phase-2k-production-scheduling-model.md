15. Phase 2K: Production Scheduling Model
Goal

Define a deterministic but manageable production-delay model.

15.1 Scheduling assumptions

For the MVP:

A production order has a planned start and planned completion.
Required materials must be available before production starts.
Each facility has a daily finished-unit capacity.
Production orders are processed according to deterministic priority.
Preemption of in-progress production is not permitted.
Setup-time optimization is deferred.
15.2 Material-ready time
MaterialReadyTimep=max⁡c∈BOM(p)ComponentAvailableTimep,cMaterialReadyTime_p = \max_{c \in BOM(p)} ComponentAvailableTime_{p,c}MaterialReadyTimep​=c∈BOM(p)max​ComponentAvailableTimep,c​
15.3 Capacity-ready time

The earliest time the facility has sufficient production capacity.

This is based on:

Orders already in progress
Higher-priority orders
Facility daily capacity
Remaining production quantities
15.4 Projected start
ProjectedStartp=max⁡(PlannedStartp,MaterialReadyTimep,CapacityReadyTimep)ProjectedStart_p = \max( PlannedStart_p, MaterialReadyTime_p, CapacityReadyTime_p )ProjectedStartp​=max(PlannedStartp​,MaterialReadyTimep​,CapacityReadyTimep​)
15.5 Production duration
DurationDaysp=RemainingQuantitypFacilityDailyCapacityAllocatedpDurationDays_p = \frac{RemainingQuantity_p} {FacilityDailyCapacityAllocated_p}DurationDaysp​=FacilityDailyCapacityAllocatedp​RemainingQuantityp​​

For day-bucket MVP scheduling:

DurationDaysp=⌈RemainingQuantitypFacilityDailyCapacity⌉DurationDays_p = \left\lceil \frac{RemainingQuantity_p} {FacilityDailyCapacity} \right\rceilDurationDaysp​=⌈FacilityDailyCapacityRemainingQuantityp​​⌉
15.6 Projected completion
ProjectedCompletionp=ProjectedStartp+DurationpProjectedCompletion_p = ProjectedStart_p + Duration_pProjectedCompletionp​=ProjectedStartp​+Durationp​
15.7 Production delay
ProductionDelayHoursp=max⁡(0,ProjectedCompletionp−PlannedCompletionp)ProductionDelayHours_p = \max( 0, ProjectedCompletion_p - PlannedCompletion_p )ProductionDelayHoursp​=max(0,ProjectedCompletionp​−PlannedCompletionp​)

User-facing days may be:

ProductionDelayDaysp=ProductionDelayHoursp24ProductionDelayDays_p = \frac{ProductionDelayHours_p}{24}ProductionDelayDaysp​=24ProductionDelayHoursp​​

Do not mix rounded and unrounded values.

15.8 Priority

Recommended ordering:

In-progress order
Explicit production-order priority
Earliest associated customer promised date
Planned start
Production-order ID
Deliverables
Plain Text
docs/domain/production-scheduling-model.md
docs/domain/production-priority-policy.md
Exit gate
Material and capacity constraints are both considered.
The schedule is deterministic.
Ties have a stable resolution.
Existing completed output is preserved.
The model explicitly documents day-bucket simplification.
