24. Phase 5T: Performance and Scalability Evaluation
Goal

Ensure the engine is fast enough for an interactive judge demonstration.

Test scales
Plain Text
tiny
demo
standard
stress
Performance measurements

Measure separately:

State reconstruction
Disruption resolution
Inventory projection
Material allocation
Production scheduling
Customer fulfilment
Financial calculation
Causal trace construction
Persistence
Total runtime
Initial targets
Operation	Demo p95	Standard p95
State reconstruction	<500 ms	<1.5 s
Disruption resolution	<100 ms	<300 ms
Inventory projection	<500 ms	<1.5 s
Production scheduling	<1 s	<3 s
Customer/SLA impact	<300 ms	<1 s
Causal trace build	<300 ms	<1 s
Full do-nothing calculation	<2 s	<6 s

The demo target is stricter than the standard benchmark because the judge-facing experience must feel immediate.

Reporting requirements

Every benchmark report must include:

Hardware
CPU
Memory
Operating system
Python version
Db2 version
Dataset version
Rule-set version
Warm or cold run
Scenario counts
Median
p95
Maximum
Error rate
Memory target

The standard dataset engine should operate within a documented memory envelope, initially:

Plain Text
Target peak application memory: <1.5 GB

If higher, document why and optimize state loading.

Performance principles

Prioritize:

Correctness
Determinism
Explainability
Performance

Do not remove intermediate evidence merely to improve latency.

Deliverables
Plain Text
artifacts/phase-5/performance/
├── demo-performance.json
├── standard-performance.json
├── stress-performance.json
└── performance-report.md
