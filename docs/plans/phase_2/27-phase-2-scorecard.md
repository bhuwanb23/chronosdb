27. Phase 2 Scorecard
Category	Weight
Domain-language precision	8
Entity and relationship completeness	12
Temporal-model correctness	12
Inventory and allocation logic	12
BOM and production logic	12
Customer and financial logic	10
Causal-model completeness	12
Intervention and counterfactual model	10
Golden-scenario validation	8
Traceability and testability	4
Total	100
Passing threshold
Plain Text
95–100: Pass
90–94: Conditional pass
Below 90: Fail
Automatic failures

Phase 2 fails regardless of score if:

Baseline and do-nothing remain confused.
No deterministic inventory equation exists.
Revenue at risk remains undefined.
Missing data is treated as zero.
A recommendation can violate a hard constraint.
Operational facts can be modified by simulation.
Causal traces skip intermediate dependencies.
Scenario time semantics remain undefined.
Golden scenario cannot be manually solved.
Independent golden-scenario calculations disagree.
Partial fulfilment is possible but not modelled or explicitly prohibited.
Intervention cost double-counting remains unresolved.
Phase 3 would need to invent business rules.
