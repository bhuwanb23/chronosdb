25. Phase 5U: Testing and Adversarial Validation
Goal

Prove correctness, safety, and predictable failure behavior.

25.1 Unit tests

Test:

Outstanding quantity
Disrupted arrival
Inventory delta
BOM requirement
Batch requirement
Material-ready time
Capacity-ready time
Projected start
Projected completion
Late quantity
Delay hours
Revenue at risk
Stable tie-breaking
Canonical result hashing
25.2 Property-based tests

Useful invariants:

Inventory conservation
Ending=Opening+In−OutEnding = Opening + In - OutEnding=Opening+In−Out
Allocation bound
Allocated≤EligibleAvailableAllocated \le EligibleAvailableAllocated≤EligibleAvailable
Production bound
Completed≤PlannedCompleted \le PlannedCompleted≤Planned
Customer fulfilment bound
OnTime+Late≤OpenQuantityOnTime + Late \le OpenQuantityOnTime+Late≤OpenQuantity
Revenue bound
0≤RevenueAtRisk≤OpenRevenue0 \le RevenueAtRisk \le OpenRevenue0≤RevenueAtRisk≤OpenRevenue
Time ordering
Completion≥StartCompletion \ge StartCompletion≥Start Delivery≥ProductAvailabilityDelivery \ge ProductAvailabilityDelivery≥ProductAvailability
Disruption monotonicity under controlled conditions

If all other inputs remain fixed and a receipt is delayed further, the engine must not calculate earlier component availability.

This does not mean every customer outcome must become worse because unused inventory may absorb the delay.

25.3 Integration tests

Test:

State reconstruction from Db2
Impact run persistence
Golden scenario
Historical replay
Restart and rerun
Failed persistence
Idempotent request
Rule-version selection
25.4 Adversarial tests
Unknown supplier

Expected:

Plain Text
REJECTED
UNKNOWN_SUPPLIER
Negative duration

Expected:

Plain Text
REJECTED
INVALID_DISRUPTION_INTERVAL
Missing inventory state

Expected:

Plain Text
PARTIALLY_COMPLETED or REJECTED
MISSING_CRITICAL_DATA

depending on scope.

Missing BOM

Affected production calculation:

Plain Text
INSUFFICIENT_DATA
Duplicate inventory event

Expected:

Detected by event identity
Not counted twice
Overlapping BOM versions

Expected:

Plain Text
INVALID_OPERATIONAL_STATE
Purchase order fully received

Expected:

Not affected by the future outage
Partial receipt

Expected:

Only outstanding quantity is delayed
No-impact outage

Expected:

Plain Text
0 operational shortages
0 new SLA breaches
₹0 disruption-caused revenue at risk
Pre-existing late order

Expected attribution:

Plain Text
PRE_EXISTING

not DISRUPTION_CAUSED.

Horizon shortage

Expected:

Plain Text
NOT_COMPLETED_WITHIN_HORIZON

No fabricated completion date.

Concurrent identical requests

Expected:

One stable business result
No inconsistent duplicates
Test targets
Plain Text
Critical path test pass rate: 100%
Golden test pass rate: 100%
Supported benchmark numerical fidelity: 100%
Flaky tests: 0
Severity-1 defects: 0
Deliverables
Plain Text
tests/impact/
├── unit/
├── property/
├── integration/
├── golden/
├── benchmark/
├── temporal/
└── adversarial/
