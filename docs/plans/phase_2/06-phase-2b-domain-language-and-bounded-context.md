6. Phase 2B: Domain Language and Bounded Context
Goal

Create a controlled vocabulary so every term has one meaning.

6.1 Bounded context

The MVP models a simplified manufacturing supply-chain planning context.

It includes:

Plain Text
Supplier procurement
→ Inbound replenishment
→ Warehouse inventory
→ Material allocation
→ Production fulfilment
→ Customer-order delivery

It does not attempt to model:

Full accounting
Detailed transportation routing
Customs clearance
Supplier-contract negotiation
Machine-level production
Workforce scheduling
Product returns
Invoice settlement
6.2 Ubiquitous language
Supplier

An organization approved to provide one or more components.

Component

A purchased or stocked material consumed to produce a finished product.

Product

A finished good associated with a bill of materials.

Bill of materials

A versioned definition of the components and quantities required to produce one unit of a product.

Warehouse

A location holding component inventory.

Facility

A location executing production orders.

Inventory lot

A time- and location-specific quantity of a component.

On-hand inventory

Physical quantity recorded at a warehouse.

Reserved inventory

Quantity committed to demand and unavailable to unrelated demand.

Available inventory

Quantity that may be allocated after reservations and applicable controls.

Safety stock

Minimum inventory that should remain after an optional transfer or allocation.

Purchase order

A planned inbound quantity from a supplier.

Production order

An instruction to produce a quantity of a finished product at a facility.

Customer order

A customer commitment for a product quantity and promised delivery date.

Supplier outage

A time-bounded event that prevents or delays specified supply from a supplier.

Scenario

An immutable definition of an operational state, disruption, objective and constraints.

Intervention

A proposed change intended to reduce disruption impact.

Simulation run

A deterministic evaluation of one scenario and one intervention.

Baseline

The projected operational outcome without the new disruption.

Do-nothing case

The projected operational outcome with the disruption but without a recovery intervention.

These two terms must not be confused.

Revenue at risk

The allocated order-line revenue associated with projected late or unfulfilled quantity.

It is not confirmed revenue loss.

SLA breach

A projected delivery condition that violates the applicable customer-service commitment.

Feasible intervention

An intervention satisfying every applicable hard constraint.

Recommendation

The highest-ranked feasible intervention under the chosen objective.

Deliverables
Plain Text
docs/domain/domain-glossary.md
docs/domain/bounded-context.md
Terminology gate
Every major term has exactly one definition.
Baseline and do-nothing are distinct.
Revenue at risk and revenue lost are distinct.
Facts and projections are distinguishable.
Scenario and intervention are distinct.
Warehouse and production facility are distinct.
