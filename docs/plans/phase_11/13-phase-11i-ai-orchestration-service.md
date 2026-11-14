13. Phase 11I: AI Orchestration Service

Expose Phase 9.

Natural Language Endpoint
POST /api/v1/explain


Request

{
  "query":"Supplier S-104 down for two weeks"
}


Pipeline

Planner
Validator
Impact
Simulation
Optimization
Evidence
Narrator
Verifier


Response

{
  "narrative":"...",
  "verification_status":"VERIFIED"
}

