31. Phase 2 Final Gate Checklist
Language and scope
 Bounded context is explicit.
 Domain glossary is complete.
 Baseline and do-nothing are distinct.
 Revenue at risk and loss are distinct.
 Facts, projections and assumptions are distinguishable.
Entity model
 Every core entity has an identifier.
 Every important attribute has a business meaning.
 Cardinalities are documented.
 Versioned relationships are explicit.
 Value objects contain their units.
Temporal model
 Event time is defined.
 Reported time is defined.
 Effective time is defined.
 Scenario as-of time is defined.
 Simulation horizon is defined.
 Time zone policy is defined.
 Boundary intervals are defined.
 Late-arriving data behavior is defined.
Inventory and BOM
 Available inventory formula is frozen.
 Projected balance formula is frozen.
 Allocation priority is frozen.
 Transferable quantity is defined.
 Shortage date is defined.
 BOM selection rule is defined.
 Component requirement formula is frozen.
 Partial production policy is explicit.
Production and customer impact
 Material-ready time is defined.
 Capacity-ready time is defined.
 Production delay is defined.
 Projected delivery is defined.
 SLA breach is defined.
 Partial fulfilment behavior is defined.
 Revenue-at-risk formula is frozen.
Causality
 Causal graph is complete.
 Every edge has a rule.
 Every impact can trace to source records.
 Contextual evidence cannot create operational facts.
 No direct unsupported jump to revenue impact exists.
Interventions
 Do-nothing is defined.
 Inventory transfer is defined.
 Expedition is defined.
 Alternate supply is defined.
 Rescheduling is defined.
 Hybrid intervention is defined.
 Feasibility reasons are defined.
 Hard and soft constraints are separated.
Counterfactual model
 Baseline state is immutable.
 Disruption overlay is fixed per scenario.
 Candidate overlays are isolated.
 Comparison basis is common.
 Outcome deltas name their reference case.
 Deterministic replay is defined.
Measures and evidence
 All numerical outputs have formulas.
 All formulas have units.
 Cost components are non-overlapping.
 Provenance model is complete.
 Missing values are not treated as zero.
 Confidence classifications are evidence-based.
Golden scenario
 Input state is complete.
 No-disruption baseline is calculated.
 Do-nothing result is calculated.
 Every intervention is calculated.
 Expected recommendation is calculated.
 Causal traces are complete.
 Two independent calculations agree.
 Golden JSON outputs are frozen.
Quality
 Domain completeness is 100%.
 Formula coverage is 100%.
 Causal coverage is 100%.
 Priority 0 ambiguity is 0%.
 Traceability coverage is 100%.
 Phase 2 score is at least 95.
 No automatic-failure condition remains.
