# AI Authority and Control Contract

This contract applies to any future AI integration. The Phase 0 application
does not require an LLM to run its health or foundation workflow.

## Authority boundary

```text
User request
  -> AI interpretation (optional)
  -> validated structured scenario
  -> deterministic Db2/Python calculations
  -> verified result
  -> AI explanation (optional)
```

The AI may interpret and explain. Deterministic services own operational truth.

## Scenario planner

| Classification | Behavior |
|---|---|
| ALLOWED | Extract supplier reference, duration, start time, objective, and constraints |
| ALLOWED | Ask for missing required information |
| VALIDATED | Return typed structured output for schema and domain validation |
| FORBIDDEN | Invent identifiers, budgets, dates, or operational facts |
| FORBIDDEN | Calculate impact, score candidates, or select an intervention |
| FORBIDDEN | Write operational or audit records without validated application code |
| FALLBACK_AVAILABLE | Use the structured scenario form when AI is unavailable |

## Evidence selector

| Classification | Behavior |
|---|---|
| ALLOWED | Formulate a retrieval query and rank contextual relevance |
| VALIDATED | Apply supplier, component, date, status, and access filters |
| FORBIDDEN | Treat retrieved text as current operational truth |
| FORBIDDEN | Use expired or unauthorized documents without a visible warning |
| FORBIDDEN | Convert historical observations into current facts |
| FALLBACK_AVAILABLE | Use predefined structured evidence queries |

## Decision narrator

| Classification | Behavior |
|---|---|
| ALLOWED | Explain verified calculations and summarize comparisons |
| ALLOWED | Explain trade-offs, warnings, and remaining risks |
| VALIDATED | Use only fields approved from structured results |
| FORBIDDEN | Introduce a new number or change a score |
| FORBIDDEN | Mark an infeasible candidate feasible or hide warnings |
| FORBIDDEN | Claim certainty not present in the result |
| FALLBACK_AVAILABLE | Use a deterministic template summary |

## Numerical claim contract

Every numerical statement must follow this chain:

```text
Claim
 -> structured result field
 -> scenario or simulation run
 -> calculation rule version
 -> source evidence
```

If any link is missing, the number is not displayed. Verification failure is
audited and the statement is removed or replaced with a non-numerical message.

## AI failure behavior

When AI is unavailable, the system still accepts structured scenarios, validates
them, calculates deterministic impact, compares interventions, preserves
evidence and audit records, and produces a templated summary. AI availability
must never determine whether a business calculation is considered true.
