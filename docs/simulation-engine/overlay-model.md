# Overlay Model

ChronosDB does not mutate operational data. Instead:

```
State + Overlay = Simulation State
```

## Overlay Categories

### Inventory Overlay

```json
{
  "action": "TRANSFER_INVENTORY",
  "component_id": "CMP-MCU-42",
  "quantity": "320",
  "from_warehouse": "WH-CHENNAI",
  "to_warehouse": "WH-PUNE"
}
```

### Expedition Overlay

```json
{
  "action": "EXPEDITE_PO",
  "purchase_order_id": "PO-2208",
  "lead_time_reduction_days": 5
}
```

### Alternate Supplier Overlay

```json
{
  "action": "ACTIVATE_ALT_SUPPLIER",
  "supplier_id": "SUP-0208",
  "component_id": "CMP-MCU-42",
  "available_quantity": "300"
}
```

### Reschedule Overlay

```json
{
  "action": "RESCHEDULE_PRODUCTION",
  "production_order_id": "MO-0882",
  "priority": 1
}
```

## Schema

See `schemas/simulation-overlay.schema.json`.