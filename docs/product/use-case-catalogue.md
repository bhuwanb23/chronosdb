# Use-Case Catalogue

Each use case is a contract for later implementation and testing. It does not
define database tables or API shapes.

## UC-001 Create supplier-outage scenario

**Actor:** Supply-chain operations manager  
**Preconditions:** Supplier and operational state exist.  
**Trigger:** User submits supplier, duration, objective, and constraints.  
**Main flow:** Validate inputs, preserve the state reference, and create an
immutable scenario ID.  
**Alternate flows:** Unknown supplier, invalid duration, missing objective,
invalid constraint, unavailable historical state.  
**Postcondition:** A valid scenario exists or a specific validation error is
returned.  
**Requirements:** FR-SCN-001–FR-SCN-010  
**Future tests:** scenario creation, validation, immutability, duplication.

## UC-002 Calculate do-nothing impact

**Actor:** System on behalf of operations manager  
**Preconditions:** Valid scenario and required operational records exist.  
**Trigger:** User requests baseline analysis.  
**Main flow:** Resolve dependencies, project inventory, calculate production and
customer effects, and persist the trace.  
**Alternate flows:** No impact, incomplete data, conflicting records.  
**Postcondition:** A reproducible baseline or explicit status exists.  
**Requirements:** FR-IMP-001–FR-IMP-014  
**Future tests:** golden scenario, no-impact case, incomplete data.

## UC-003 Generate and validate intervention candidates

**Actor:** System  
**Preconditions:** Baseline exists.  
**Trigger:** Baseline calculation completes.  
**Main flow:** Generate candidate types and classify each as feasible,
infeasible, or insufficient data with reasons.  
**Alternate flows:** No inventory, no approved alternate supplier, impossible
budget.  
**Postcondition:** Candidate set is complete and inspectable.  
**Requirements:** FR-INT-001–FR-INT-011  
**Future tests:** safety-stock, approval, budget, and capacity constraints.

## UC-004 Compare intervention outcomes

**Actor:** Supply-chain operations manager  
**Preconditions:** Candidate simulations use the same baseline.  
**Trigger:** User opens comparison.  
**Main flow:** Display normalized cost, delay, SLA, revenue, feasibility, and
risk metrics.  
**Alternate flows:** One candidate fails; successful candidates remain visible.  
**Postcondition:** Comparable candidate results are available.  
**Requirements:** FR-SIM-001–FR-SIM-007  
**Future tests:** repeatability and candidate isolation.

## UC-005 Recommend an intervention

**Actor:** System for human review  
**Preconditions:** At least one feasible candidate exists.  
**Trigger:** User selects an objective.  
**Main flow:** Rank feasible candidates, expose objective and constraints, and
return the selected candidate with trade-offs.  
**Alternate flows:** No feasible candidate, tie, or missing metric.  
**Postcondition:** A recommendation or explicit no-recommendation status exists.  
**Requirements:** FR-OPT-001–FR-OPT-008  
**Future tests:** objective ranking, tie handling, no-feasible case.

## UC-006 Inspect evidence

**Actor:** Operations manager or auditor  
**Preconditions:** A baseline or candidate result exists.  
**Trigger:** User opens an evidence reference.  
**Main flow:** Show Db2 source records, rule version, calculation trace, and
controlled documents where available.  
**Alternate flows:** Evidence unavailable or unauthorized.  
**Postcondition:** The user sees a truthful evidence status; no link is
fabricated.  
**Requirements:** FR-EVD-001–FR-EVD-009  
**Future tests:** source-link coverage and unavailable evidence.

## UC-007 Replay a completed decision

**Actor:** Auditor or operations manager  
**Preconditions:** Completed scenario and audit records exist.  
**Trigger:** User opens a historical decision.  
**Main flow:** Load stored stages and outputs without recomputation or mutation.  
**Alternate flows:** Missing audit record or incompatible rule version.  
**Postcondition:** Original decision remains unchanged and reviewable.  
**Requirements:** FR-AUD-001–FR-AUD-008  
**Future tests:** replay consistency and audit immutability.

## UC-008 Handle insufficient data

**Actor:** System  
**Preconditions:** A required fact, relationship, or evidence source is absent.  
**Trigger:** Calculation or validation reaches the missing input.  
**Main flow:** Identify the missing data and mark the affected result.  
**Postcondition:** The system distinguishes `NO_IMPACT`,
`NO_FEASIBLE_INTERVENTION`, `INSUFFICIENT_DATA`, and `SIMULATION_FAILED`.

## UC-009 Operate without an LLM

**Actor:** Operations manager  
**Preconditions:** Structured input and deterministic services are available.  
**Trigger:** LLM service is unavailable or disabled.  
**Main flow:** Use structured scenario input, deterministic calculations,
comparison, evidence, audit, and a templated summary.  
**Postcondition:** Core decision support remains usable without generated prose.
