# Phase 7C: Objective Model

## Supported Objectives

- `MINIMIZE_REVENUE_RISK`
- `MINIMIZE_SLA_BREACHES`
- `MINIMIZE_DELAY`
- `MINIMIZE_COST`
- `MAXIMIZE_SERVICE_LEVEL`
- `BALANCED_RECOVERY` (default)

Each objective maps to five explicit weights in
`src/backend/chronosdb/optimization/contracts.py`:

```json
{
  "objective": "BALANCED_RECOVERY",
  "weights": {
    "revenue": 0.40,
    "sla": 0.30,
    "cost": 0.15,
    "delay": 0.10,
    "risk": 0.05
  }
}
```

## Validation Rules

- Every weight must be finite and within `[0, 1]`.
- The five weights must sum to `1.0` within `1e-9`.
- Negative weights, weights above 1.0, and sums other than 1.0 raise
  `OptimizationValidationError`.
- Unknown objective names raise `OptimizationValidationError`.

Schema: `schemas/objective.schema.json`.
