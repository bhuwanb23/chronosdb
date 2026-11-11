10. Phase 2F: Unit, Quantity and Financial Model
Goal

Prevent silent unit errors and misleading financial calculations.

10.1 Unit-of-measure policy

Each component has one canonical inventory unit.

Examples:

Plain Text
EA = each
KG = kilogram
L = litre
M = metre

MVP recommendation:

Use EA for all golden-scenario electronic components.
Do not introduce conversion unless required.
Reject incompatible units.
10.2 Quantity precision

Recommended conceptual precision:

Plain Text
Component quantity: decimal, not floating point
Product quantity: integer for discrete finished goods
Money: fixed decimal
Percentages: decimal from 0 to 1
10.3 Currency policy

Use one canonical MVP currency:

Plain Text
INR

All costs and revenue values in the golden dataset use INR.

Multi-currency conversion is deferred.

10.4 Rounding policy
Preserve full internal decimal precision.
Round money only for presentation.
Use two decimal places for INR calculations.
Do not round intermediate quantities unless the component requires integer units.
Round projected timestamps only if the scheduling model defines it.
10.5 Financial distinctions
Order-line revenue
Rline=Qordered×PunitR_{line} = Q_{ordered} \times P_{unit}Rline​=Qordered​×Punit​
Late quantity revenue at risk
RARline=Qlate×PunitRAR_{line} = Q_{late} \times P_{unit}RARline​=Qlate​×Punit​

Do not automatically classify the entire order-line revenue as at risk when only part of the quantity is late.

Intervention cost

May include:

Alternate supplier price premium
Expedite fee
Transfer transportation cost
Rescheduling penalty
Overtime cost, if modelled

MVP recommendation:

Cintervention=Cpurchase premium+Cexpedite+Ctransfer+CrescheduleC_{intervention} = C_{purchase\ premium} + C_{expedite} + C_{transfer} + C_{reschedule}Cintervention​=Cpurchase premium​+Cexpedite​+Ctransfer​+Creschedule​
Deliverable
Plain Text
docs/domain/units-and-financial-model.md
Exit gate
Every quantity has a unit.
Every monetary value has a currency.
Revenue at risk supports partial quantity.
Costs are not double-counted.
Rounding rules are explicit.
