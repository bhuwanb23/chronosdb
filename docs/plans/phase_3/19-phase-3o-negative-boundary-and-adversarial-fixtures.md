19. Phase 3O: Negative, Boundary and Adversarial Fixtures
Goal

Ensure later systems fail safely rather than producing plausible nonsense.

Required categories
Invalid entity references
Unknown supplier
Unknown component
Unknown warehouse
Unknown production order
Unknown scenario
Invalid quantities
Negative inventory
Zero ordered quantity
Negative disruption duration
Transfer exceeding source stock
Completed quantity exceeding planned quantity
Invalid time
Arrival before order
Scenario before entity activation
Promised delivery before customer order
Outage end before start
Overlapping BOM versions
Missing critical data
No active BOM
No inventory snapshot
Missing promised date
Missing supplier approval
Missing intervention cost
Contradictions
Supplier marked inactive but agreement active
Purchase order marked received with outstanding quantity
Inventory transaction and snapshot disagree
Production completed without required materials
Transfer receipt without dispatch
Optimization traps
Cheapest intervention violates SLA minimum
Best SLA intervention exceeds budget
Two candidates tie
No feasible candidate
Candidate improves one order but harms a higher-priority order
Negative supplier premium due to cheaper alternate supply
Retrieval traps
Expired policy that appears highly relevant
Unauthorized incident report
Historical incident mentioning same supplier but unrelated component
Prompt injection inside a synthetic supplier notice
Document claiming an operational fact contradicted by structured records
Expected error labels
Plain Text
UNKNOWN_ENTITY
INVALID_QUANTITY
INVALID_INTERVAL
MISSING_CRITICAL_DATA
CONTRADICTORY_STATE
INFEASIBLE_INTERVENTION
NO_FEASIBLE_INTERVENTION
INSUFFICIENT_DATA
UNAUTHORIZED_EVIDENCE
EXPIRED_EVIDENCE
Deliverables
Plain Text
data/fixtures/
├── invalid/
├── boundary/
├── adversarial/
└── expected_errors.json
