7. Phase 7C: Objective Model

Objectives must be explicit.

Supported Objectives
MINIMIZE_REVENUE_RISK

MINIMIZE_SLA_BREACHES

MINIMIZE_DELAY

MINIMIZE_COST

MAXIMIZE_SERVICE_LEVEL

BALANCED_RECOVERY

Objective Object
{
  "objective":"BALANCED_RECOVERY",
  "weights":{
    "revenue":0.40,
    "sla":0.30,
    "cost":0.15,
    "delay":0.15
  }
}

Rule

Weights always sum to:

1.0

Deliverables
schemas/objective.schema.json

docs/optimization/objectives.md

