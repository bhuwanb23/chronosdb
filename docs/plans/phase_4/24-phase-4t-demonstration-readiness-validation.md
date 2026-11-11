24. Phase 4T: Demonstration-Readiness Validation
Goal

Verify that the dataset produces an effective judge experience.

Ten-second comprehension test

A reviewer should be able to identify:

Which supplier failed
Which component is constrained
How many customer orders are at risk
How much revenue is at risk
Which intervention is recommended

Target:

Plain Text
5/5 reviewers identify all five correctly
Scenario-comparison test

A reviewer should be able to explain:

Why transfer-only is insufficient
Why the 500-unit transfer is infeasible
Why alternate supply alone is insufficient
Why the hybrid is selected
Why the selected plan satisfies budget

Target:

Plain Text
At least 4/5 reviewers answer correctly
Evidence-navigation test

Using only the dataset artifacts, a reviewer should locate:

Purchase order causing changed supply
Inventory record controlling transfer feasibility
BOM record creating component demand
Production order creating customer impact
Customer line creating revenue exposure
Procedure supporting intervention

Target:

Plain Text
Median time below 3 minutes before the UI exists

Later UI phases should reduce this dramatically.

Demo stability test

Run the golden-data assembly and oracle ten times.

Required:

Plain Text
Expected result: 10/10 identical
Runtime failure: 0
Checksum variation: 0
Deliverables
Plain Text
artifacts/phase-4/demo-readiness/
├── reviewer-results.csv
├── comprehension-report.md
├── evidence-navigation-report.md
└── stability-report.json
