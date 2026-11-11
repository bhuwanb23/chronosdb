# Phase 2P: Objective and Ranking Model

## Hard-constraint filter

Before ranking, remove any candidate that violates approval, capacity,
inventory, budget, safety-stock, horizon, or valid-state-transition rules.
Candidates with missing required facts are `INSUFFICIENT_DATA`, not
infeasible. No candidate that fails a hard constraint may be recommended.

## Objective modes

### MINIMIZE_SLA_BREACHES

Lexicographic order:

1. fewest breached customer orders;
2. lowest revenue at risk;
3. lowest intervention cost;
4. lowest total delay;
5. stable intervention ID.

### MINIMIZE_REVENUE_AT_RISK

1. lowest revenue at risk;
2. fewest breached customer orders;
3. lowest cost;
4. lowest delay;
5. stable intervention ID.

### MINIMIZE_RECOVERY_COST

1. lowest intervention cost;
2. subject to the configured service-level constraint;
3. lowest revenue at risk;
4. lowest delay;
5. stable intervention ID.

### BALANCED_RECOVERY

Normalize each candidate metric to `[0,1]`, lower is better:

```text
normalized(x_i) = (x_i - min(x)) / (max(x) - min(x))
```

When all candidates have the same value, normalized value is zero.

```text
score =
    0.40 * sla_breach_score
  + 0.30 * revenue_risk_score
  + 0.20 * delay_score
  + 0.10 * recovery_cost_score
```

Weights sum to one and must be stored with the result.

## Ties

Equal metrics produce a visible tie. If one recommendation is required, use
the stable intervention ID only after reporting the tie. Pareto-equivalent
plans remain valid alternatives.

## Golden-scenario default

The corrected golden scenario uses `MINIMIZE_SLA_BREACHES`, a ₹200,000 budget,
approved suppliers only, enforced minimum source safety stock, and a 30-day
horizon.
