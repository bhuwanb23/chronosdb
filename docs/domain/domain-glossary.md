# Domain Glossary

| Term | Definition |
|---|---|
| Supplier | Approved organization that provides one or more components. |
| Component | Purchased or stocked material consumed to make a finished product. |
| Product | Finished good with a versioned bill of materials. |
| Bill of materials | Versioned components and quantities required for one product unit. |
| Warehouse | Location holding component inventory. |
| Facility | Location executing production orders. |
| Inventory lot | Time- and location-specific quantity of a component. |
| On-hand inventory | Physical quantity recorded at a warehouse. |
| Reserved inventory | Quantity committed to demand and unavailable to unrelated demand. |
| Available inventory | On-hand quantity after reservations and applicable controls. |
| Safety stock | Minimum quantity intended to remain after an optional transfer. |
| Purchase order | Planned inbound quantity from a supplier. |
| Production order | Instruction to produce a product quantity at a facility. |
| Customer order | Customer commitment for a product quantity and promised delivery. |
| Supplier outage | Time-bounded event that prevents or delays specified supplier supply. |
| Operational state | Facts and plans valid and known at a selected point in time. |
| Scenario | Immutable operational-state reference, disruption, objective, and constraints. |
| Intervention | Proposed change intended to reduce disruption impact. |
| Simulation run | Deterministic evaluation of one scenario and one intervention. |
| Baseline | Projection without the new disruption. |
| Do-nothing case | Projection with the disruption and no recovery intervention. |
| Shortage | Requirement that cannot be fully allocated by its required time. |
| Projected delay | Difference between projected and committed completion/delivery time. |
| SLA breach | Projected delivery that violates the applicable service commitment. |
| Revenue at risk | Revenue for projected late or unfulfilled quantity; not confirmed loss. |
| Feasible intervention | Intervention satisfying every applicable hard constraint. |
| Recommendation | Highest-ranked feasible intervention under the selected objective. |
| Evidence | Source record or controlled document supporting a fact or result. |
| Fact | Recorded operational observation or approved plan value. |
| Projection | Derived future state calculated from facts, rules, and scenario inputs. |

## Non-equivalences

- Baseline is not the do-nothing case.
- Revenue at risk is not revenue lost.
- A facility is not a warehouse.
- A scenario is not an intervention.
- A fact is not a projection.
- Infeasible is not the same as insufficient data.
