10. Phase 11F: Simulation Service

Expose Phase 6.

Run Simulation

POST /api/v1/scenarios/{id}/simulate


Request

{
  "intervention":"TRANSFER"
}


Response

{
  "simulation_id":"SIM-001"
}


Multi-Simulation

POST /api/v1/scenarios/{id}/simulate-all


Returns

Transfer
Expedite
Supplier
Reschedule
Hybrid

