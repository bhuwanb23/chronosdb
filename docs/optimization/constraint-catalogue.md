# Phase 7D: Constraint Registry

## Constraint Categories
- Cost
- Inventory
- Supplier
- Warehouse
- Capacity
- Delay
- Regulatory

## Example Constraint
```yaml
constraint_id: CON-001
name: max_recovery_cost
value: 200000 INR
operator: <=
```

## Typical Constraints
- Recovery cost ≤ ₹2 lakh
- Safety stock ≥ minimum
- Supplier approved
- Transfer lane approved
- Delay ≤ 10 days
- Capacity utilization ≤ 100%

## Deliverable
config/constraints/
docs/optimization/constraint-catalogue.md

## Phase 7D Status: IMPLEMENTED
