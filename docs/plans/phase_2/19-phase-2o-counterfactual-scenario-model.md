19. Phase 2O: Counterfactual Scenario Model
Goal

Define how alternative futures are generated without modifying operational truth.

19.1 Scenario composition

A scenario consists of:

Scenario=BaselineState+Disruption+Objective+Constraints+SimulationHorizon+RuleVersionScenario = BaselineState + Disruption + Objective + Constraints + SimulationHorizon + RuleVersionScenario=BaselineState+Disruption+Objective+Constraints+SimulationHorizon+RuleVersion

An intervention run consists of:

CounterfactualRun=Scenario+InterventionOverlayCounterfactualRun = Scenario + InterventionOverlayCounterfactualRun=Scenario+InterventionOverlay
19.2 State layers
Layer 1: Operational state

The factual state at the scenario as_of_time.

Layer 2: Disruption overlay

Changes expected future supply.

Layer 3: Intervention overlay

Changes future receipts, transfers, allocation or schedule.

Layer 4: Derived outcome

Calculated shortages, delays, SLA breaches and financial impact.

19.3 Immutability
Layer 1 is immutable during simulation.
Layer 2 is immutable for all candidates in one scenario.
Each Layer 3 intervention is isolated.
Layer 4 is stored per run.
19.4 Comparability

All candidates within a scenario must use:

Same baseline state
Same disruption
Same simulation horizon
Same business-rule version
Same objective definitions
Same cost basis

Otherwise comparisons are invalid.

19.5 Determinism

Given identical:

Plain Text
baseline_state_version
disruption
intervention
constraint_set
rule_version

the outcome must be identical.

19.6 Outcome delta

For candidate iii:

RevenueProtectedi=RevenueAtRiskDoNothing−RevenueAtRiskiRevenueProtected_i = RevenueAtRisk_{DoNothing} - RevenueAtRisk_iRevenueProtectedi​=RevenueAtRiskDoNothing​−RevenueAtRiski​ SLABreachesAvoidedi=SLABreachesDoNothing−SLABreachesiSLABreachesAvoided_i = SLABreaches_{DoNothing} - SLABreaches_iSLABreachesAvoidedi​=SLABreachesDoNothing​−SLABreachesi​ DelayReductioni=TotalDelayDoNothing−TotalDelayiDelayReduction_i = TotalDelay_{DoNothing} - TotalDelay_iDelayReductioni​=TotalDelayDoNothing​−TotalDelayi​
Deliverable
Plain Text
docs/domain/counterfactual-model.md
Exit gate
Operational facts cannot be modified by a scenario.
Candidates share the same comparison base.
Every output has a scenario and run identity.
Same inputs produce identical outputs.
Deltas always name their reference case.
