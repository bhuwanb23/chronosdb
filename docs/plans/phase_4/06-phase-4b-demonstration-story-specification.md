6. Phase 4B: Demonstration-Story Specification
Goal

Ensure the dataset supports an understandable judge-facing business narrative.

The full dataset can contain many products and suppliers, but the primary demonstration must remain focused.

Locked demonstration story

At 08:00 IST on 11 November 2026:

Asterion Control Systems learns that supplier SUP-0104 is unavailable for 14 days.
The supplier provides critical microcontroller CMP-MCU-42.
An 800-unit purchase order is delayed.
Existing Pune inventory protects the first manufacturing order.
Later manufacturing orders become material constrained.
Two customer commitments become exposed.
ChronosDB compares transfer, alternate supply, expedition where applicable, rescheduling, and hybrid intervention.
The hybrid plan provides the best SLA outcome within the ₹200,000 recovery budget.
Every output links to the synthetic operational records and deterministic calculations that produced it.
Demonstration-data requirements

The primary scenario must visibly contain:

One clear disruption
One critical component
At least three production orders
At least three customer orders
One unaffected customer order
Two affected customer orders
At least two feasible single interventions
At least one infeasible intervention
One superior hybrid intervention
One relevant historical incident
One relevant procedure
One misleading but filtered document
Complete provenance
Judge-visible metrics

The fixture must support:

Plain Text
Affected components
Affected purchase orders
Affected production orders
Affected customer orders
Projected SLA breaches
Revenue at risk
Recovery cost
Revenue protected
Projected delay
Evidence-record count
Deliverable
Plain Text
docs/dataset-release/demo-story-contract.md
Exit gate

A reviewer must understand the disruption, consequences, alternatives, and recommendation from the dataset without inspecting generator code.

