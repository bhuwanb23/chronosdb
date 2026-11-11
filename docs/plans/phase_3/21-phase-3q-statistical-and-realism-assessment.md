21. Phase 3Q: Statistical and Realism Assessment
Goal

Ensure data is neither trivially uniform nor accidentally impossible.

Required descriptive statistics
Supply
Suppliers per component
Lead-time distribution
Price distribution
Capacity distribution
Approval distribution
Product structure
Components per BOM
BOM critical-component count
Product-family demand
Inventory
Days of coverage
Safety-stock ratio
Stockout frequency
Warehouse concentration
Operations
Production utilization
Purchase-order arrival performance
Customer-order size
Customer priority
SLA lead time
Late order rate
Disruptions
Duration
Scope
Affected records
Severity
Feasible intervention count
Impact level
Realism thresholds

Avoid:

Every component having exactly two suppliers
Every purchase order using the same quantity
Every customer order having identical revenue
Perfect historical delivery
Uniform disruption impact
All scenarios having a feasible solution
One intervention type always winning
Benchmark balance checks

Recommended constraints:

No single intervention wins more than 45% of solvable scenarios.
At least 10% of scenarios have no operational impact.
At least 5% have no feasible intervention.
At least 5% contain critical insufficient data.
At least 20% require more than simple direct dependency traversal.
At least 20% have competing objectives.
Test scenarios cover every intervention type.

These are design targets, not facts about real supply chains.

Distribution comparison

Compare generated distributions against configuration targets.

Example:

DistributionDeviation=∣ObservedShare−TargetShare∣DistributionDeviation = |ObservedShare - TargetShare|DistributionDeviation=∣ObservedShare−TargetShare∣

Recommended tolerance:

Plain Text
±5 percentage points for major categorical distributions
Deliverables
Plain Text
artifacts/dataset-statistics.json
artifacts/dataset-statistics.md
artifacts/distribution-checks.json
