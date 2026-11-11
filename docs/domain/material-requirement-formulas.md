# Phase 2J: Material-Requirement Formula Catalogue

| ID | Formula | Inputs | Output | Preconditions |
|---|---|---|---|---|
| BOM-001 | `remaining = planned - completed` | Production quantities | Remaining product quantity | Completed cannot exceed planned |
| BOM-002 | `gross = quantity * bom_qty * (1 + scrap)` | Product quantity, BOM line, scrap | Gross component requirement | Active BOM and non-negative scrap |
| BOM-003 | `required = ceil(gross)` | Gross quantity, component unit | Discrete required quantity | Component requires whole units |
| BOM-004 | `shortage = max(0, required - allocatable)` | Requirement and allocation | Shortage quantity | Same unit and consumption time |

## Formula rules

- All quantities carry a unit.
- Scrap is a decimal from zero through one and is applied once.
- A missing active BOM produces `INSUFFICIENT_DATA`, not zero demand.
- A completed quantity is not re-produced.
- Material already issued is not counted as newly required.
- Results retain the BOM version, rule version, input production order, and
  component evidence.

## Edge cases

- Zero remaining quantity produces no new material requirement.
- Negative remaining quantity is invalid data.
- A non-integer component requirement rounds upward only when that component's
  unit requires whole units.
- An optional component without a substitution rule is outside MVP behavior.
