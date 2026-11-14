7. Phase 6C: Scenario and Overlay Model

The core ChronosDB architectural innovation.

Instead of:

Change operational database


we do:

State
+
Overlay
=
Simulation State

Overlay Categories
Inventory Overlay
{
  "action":"TRANSFER_INVENTORY",
  "component_id":"CMP-MCU-42",
  "quantity":"320",
  "from_warehouse":"WH-CHENNAI",
  "to_warehouse":"WH-PUNE"
}

Expedition Overlay
{
  "action":"EXPEDITE_PO",
  "purchase_order_id":"PO-2208",
  "lead_time_reduction_days":5
}

Alternate Supplier Overlay
{
  "action":"ACTIVATE_ALT_SUPPLIER",
  "supplier_id":"SUP-0208",
  "component_id":"CMP-MCU-42",
  "available_quantity":"300"
}

Reschedule Overlay
{
  "action":"RESCHEDULE_PRODUCTION",
  "production_order_id":"MO-0882",
  "priority":1
}

Deliverables
schemas/simulation-overlay.schema.json

docs/simulation-engine/overlay-model.md

