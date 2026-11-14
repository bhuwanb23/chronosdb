8. Phase 11D: Scenario Service

Purpose:

Manage business scenarios.

Endpoint
Create Scenario
POST /api/v1/scenarios


Request

{
  "supplier_id":"SUP-0104",
  "duration_days":14,
  "objective":"MINIMIZE_SLA_BREACH"
}


Response

{
  "scenario_id":"SCN-001"
}

Additional Endpoints
GET /api/v1/scenarios/{id}

GET /api/v1/scenarios/{id}/status

DELETE /api/v1/scenarios/{id}


(Delete may be soft-delete only)

