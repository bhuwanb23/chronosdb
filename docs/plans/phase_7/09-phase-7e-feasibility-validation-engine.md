9. Phase 7E: Feasibility Validation Engine

Before scoring:

Check feasibility.

Invalid Plans Must Be Rejected

Examples:

Transfer violates safety stock

Supplier not approved

Expedite impossible

Capacity exceeded

Budget exceeded

Statuses
FEASIBLE

CONDITIONALLY_FEASIBLE

INFEASIBLE

Example
{
  "candidate":"TRANSFER",
  "status":"INFEASIBLE",
  "reason":"Safety stock violated"
}

Deliverable
src/backend/chronosdb/optimization/feasibility/
