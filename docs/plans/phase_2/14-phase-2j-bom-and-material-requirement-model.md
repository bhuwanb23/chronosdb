14. Phase 2J: BOM and Material-Requirement Model
Goal

Translate production quantity into component demand.

14.1 BOM selection

For production order ppp, select the BOM active at:

Plain Text
planned production start time

If no active BOM exists:

Plain Text
INSUFFICIENT_DATA

Do not silently select the latest BOM.

14.2 Component requirement

For product quantity QpQ_pQp​:

GrossRequirementp,c=Qp×BOMQuantityp,c×(1+ScrapFactorp,c)GrossRequirement_{p,c} = Q_p \times BOMQuantity_{p,c} \times (1 + ScrapFactor_{p,c})GrossRequirementp,c​=Qp​×BOMQuantityp,c​×(1+ScrapFactorp,c​)

For discrete components, round upward:

RequiredQuantityp,c=⌈GrossRequirementp,c⌉RequiredQuantity_{p,c} = \lceil GrossRequirement_{p,c} \rceilRequiredQuantityp,c​=⌈GrossRequirementp,c​⌉
14.3 Remaining production requirement

For partially completed production:

RemainingProductQuantity=PlannedQuantity−CompletedQuantityRemainingProductQuantity = PlannedQuantity - CompletedQuantityRemainingProductQuantity=PlannedQuantity−CompletedQuantity

Then calculate materials only for the remaining quantity unless material has already been issued.

14.4 Mandatory components

If a mandatory component is unavailable:

The affected production quantity cannot begin or complete.
Delay calculation continues until sufficient material becomes available.

Optional BOM components are out of MVP scope unless a substitution rule exists.

14.5 Substitution

Substitution is permitted only when:

Components share an approved substitution relationship.
Conversion ratio is defined.
Effective date is valid.
Product or BOM permits substitution.
Required qualification is valid.

For the MVP, alternate supplier is preferred over component substitution. Component substitution may be deferred unless needed for the golden scenario.

Deliverables
Plain Text
docs/domain/bom-model.md
docs/domain/material-requirement-formulas.md
Exit gate
The BOM version is time-valid.
Component requirement is reproducible.
Scrap factor is not double-counted.
Partial production is handled explicitly.
Missing BOM produces insufficient data, not zero demand.
