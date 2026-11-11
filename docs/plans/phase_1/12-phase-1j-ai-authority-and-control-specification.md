12. Phase 1J: AI authority and control specification
Goal

Define precisely what AI controls and what it cannot control.

AI component 1: Scenario Planner
Allowed
Extract supplier reference
Extract duration
Extract objective
Extract cost ceiling
Ask for missing required information
Return typed structured output
Forbidden
Invent supplier IDs
Invent budget
Calculate business impact
Create database records without validation
Select an intervention independently
AI component 2: Evidence selector
Allowed
Formulate retrieval query
Rank contextual relevance
Select relevant procedures or incidents
Forbidden
Treat retrieved text as operational truth
Bypass access filters
Use expired documents without warning
Convert a historical incident into a current-state fact
AI component 3: Decision narrator
Allowed
Explain verified calculations
Summarize comparisons
Explain trade-offs
Format an executive summary
Forbidden
Introduce a new number
Change a candidate score
Mark an infeasible intervention feasible
Hide warnings
Claim certainty not present in the structured output
AI failure policy

## When AI is unavailable:

| Capability | Behavior |
| --- | --- |
| Natural-language parsing | Use structured form |
| Evidence-query generation | Use predefined structured query |
| Recommendation narration | Use deterministic template |
| Simulation | Continue normally |
| Optimization | Continue normally |
| Audit | Record AI unavailability |

## Numerical claim contract

## For every number produced in narrative text:

Claim
→ Structured field
→ Simulation run
→ Calculation rule
→ Source evidence


If the chain cannot be completed, the number must not be displayed.

Deliverable
docs/product/ai-authority-contract.md

## Exit gate

## Every planned AI capability is classified as:

ALLOWED
VALIDATED
FORBIDDEN
FALLBACK_AVAILABLE

