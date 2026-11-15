# Intervention Catalogue

Simulation actions are versioned, analogous to the Phase 5 rule registry.

## Intervention Types

- `INT-TRANSFER`
- `INT-EXPEDITE`
- `INT-SUPPLIER`
- `INT-RESCHEDULE`
- `INT-HYBRID`

## Example

```yaml
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
```

## Registry

Machine-readable definitions live in `config/interventions/` and `src/chronosdb/config/interventions/registry.py`.