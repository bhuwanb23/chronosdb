19. Phase 4O: Frozen Benchmark Dataset
Goal

Produce the official dataset against which later engines are evaluated.

Required benchmark count
Plain Text
60 scenarios
Recommended distribution
Scenario group	Count
Full supplier outage	18
Partial outage	8
Component-specific outage	6
Purchase-order-specific disruption	4
Transfer-constrained case	4
Alternate-supplier-constrained case	4
Budget-constrained case	4
No-impact case	3
No-feasible-plan case	3
Insufficient-data case	3
Tie/Pareto case	3
Required benchmark partitions
Plain Text
development: 24
validation: 12
test: 18
golden: 3
adversarial-only: 3

If these categories overlap, the manifest must identify the relationship explicitly. Exclusive partitions must not overlap.

Test-set freeze

After Phase 4 release:

No expected test outcome may be changed to accommodate implementation behavior.
A discovered error requires a dataset version increase.
The implementation must adapt to the ground truth, not vice versa.
Test-case-specific branches are prohibited.
Difficulty levels

Every scenario receives:

Plain Text
L1_DIRECT
L2_CONNECTED
L3_CONSTRAINED
L4_ADVERSARIAL
Benchmark balance requirements
Every intervention type appears in test scenarios.
At least three test scenarios have no feasible intervention.
At least three contain insufficient data.
At least three contain ties or multiple valid optima.
At least five contain partial fulfilment.
At least five require temporal reconstruction.
At least five include misleading document evidence.
No intervention wins an unrealistic majority of solvable scenarios.
Deliverables
Plain Text
data/releases/v1.0.0/benchmarks/
├── scenarios/
├── expected/
├── partition_manifest.json
├── scenario_catalogue.csv
├── difficulty_labels.csv
└── benchmark_release_notes.md
