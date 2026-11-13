33. Phase 5 Final Gate Checklist
Inputs and contracts
 Dataset version is pinned.
 Dataset checksums match.
 Rule-set version is pinned.
 Request schema is complete.
 Result schema is complete.
 Runtime cannot access expected benchmark answers.
 No LLM dependency exists.
State reconstruction
 Effective master records are selected correctly.
 Information-time rules are enforced.
 Inventory reconstructs exactly.
 Outstanding purchase orders reconstruct exactly.
 Production state reconstructs exactly.
 Customer state reconstructs exactly.
 State hash matches the frozen golden state.
 Future information leakage is zero.
Disruption and supply
 Disruption interval validates.
 Scope resolves correctly.
 Fully received orders are excluded.
 Partially received orders use outstanding quantity.
 Cancelled orders are excluded.
 Recovery lag is applied exactly once.
 Original and disrupted receipts are preserved.
 Out-of-horizon receipts are handled correctly.
Inventory and materials
 Inventory events have stable ordering.
 Opening balance reconciles.
 Receipt events apply at the correct time.
 BOM selection is correct.
 Batch requirements are correct.
 Reservations are not double counted.
 Materials are not double allocated.
 Shortage timestamps are exact.
 Shortage quantities are exact.
 Physical inventory is conserved.
Production
 Batch creation is correct.
 Material-ready time is correct.
 Capacity-ready time is correct.
 Priority sorting is stable.
 Capacity is never exceeded.
 Material is consumed once.
 Projected starts are correct.
 Projected completions are correct.
 Horizon failures are explicit.
Customer and finance
 Product availability is calculated correctly.
 Customer priority is applied correctly.
 Fulfilment segments reconcile.
 Delivery lead time is applied correctly.
 SLA classification is correct.
 Partial late quantity is handled.
 Revenue at risk uses late quantity only.
 Currency remains INR.
 Revenue totals reconcile.
 Delay metrics use documented units.
Causality and provenance
 Every affected order has a causal trace.
 Every headline number has provenance.
 Pre-existing impact is distinguished.
 Disruption-caused impact is identified.
 Causal edges reference valid entities.
 Rule IDs are present.
 Input-state hash is present.
 Result hash is present.
Data quality
 Missing and zero are distinct.
 Critical missing data blocks affected calculations.
 Unaffected calculations continue safely.
 Partial runs are labelled.
 Errors are machine-readable.
 Warnings are preserved.
 Successful status never hides critical failure.
Determinism and persistence
 Golden result is stable across 100 runs.
 Benchmark sample is stable across repeated runs.
 Cross-process result is stable.
 Database restart does not change result.
 Idempotency works.
 Duplicate requests do not create inconsistent results.
 Completed output is immutable.
 Operational records remain unchanged.
Correctness and testing
 Golden output matches ground truth exactly.
 Development benchmark passes.
 Validation benchmark passes.
 Frozen test benchmark meets targets.
 Numerical fidelity is 100%.
 SLA classification is 100%.
 Failure classification is 100%.
 Property tests pass.
 Adversarial tests pass.
 Flaky tests are zero.
 Severity-1 defects are zero.
Performance
 Demo p95 is below two seconds.
 Standard p95 is below six seconds.
 Stage timings are recorded.
 Peak memory is measured.
 Performance hardware is documented.
 Correctness was not weakened for speed.
Release
 Traceability matrix is complete.
 Benchmark report is complete.
 Determinism report is complete.
 Performance report is complete.
 Independent review is signed off.
 Phase 5 score is at least 95.
 No automatic-failure condition remains.
