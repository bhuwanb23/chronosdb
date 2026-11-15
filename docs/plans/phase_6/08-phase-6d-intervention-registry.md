8. Phase 6D: Intervention Registry

Exactly as Phase 5 used Rule Registry.

Simulation actions must be versioned.

Intervention Types
INT-TRANSFER
INT-EXPEDITE
INT-SUPPLIER
INT-RESCHEDULE
INT-HYBRID


Example

intervention_id: INT-TRANSFER
version: 1.0.0

inputs:
  component_id
  quantity
  source_warehouse
  destination_warehouse

validation:
  transferable_inventory > quantity
  remaining_after_transfer >= safety_stock

Deliverables
config/interventions/

docs/simulation-engine/intervention-catalogue.md

