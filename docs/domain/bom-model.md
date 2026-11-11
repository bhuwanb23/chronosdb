# Phase 2J: BOM and Material-Requirement Model

## BOM selection

For production order `p`, select the BOM version active at the planned
production start time. If no version is active, return `INSUFFICIENT_DATA`; do
not select the latest version as a fallback.

## Requirements

For product quantity `Q` and component `c`:

```text
gross_requirement(Q,c) =
    Q * bom_quantity_per_product(c) * (1 + scrap_factor(c))
```

For discrete components:

```text
required_quantity(Q,c) = ceil(gross_requirement(Q,c))
```

Scrap is applied exactly once at the material-requirement boundary.

## Partial production

```text
remaining_product_quantity =
    planned_quantity - completed_quantity
```

Material is calculated for the remaining quantity unless a separate material
issue/allocation record proves that it was already consumed.

## Mandatory components

If a mandatory component is unavailable, the affected production quantity
cannot begin or complete. The delay continues until sufficient material is
available. Optional components are outside the MVP unless an explicit
substitution rule exists.

## Substitution

Component substitution requires:

- approved substitution relationship;
- valid conversion ratio;
- effective date;
- BOM or product permission;
- required qualification.

The MVP prefers alternate suppliers over component substitution. If a required
substitution fact is missing, return `INSUFFICIENT_DATA`.
