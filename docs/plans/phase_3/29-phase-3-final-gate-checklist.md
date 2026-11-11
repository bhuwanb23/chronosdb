29. Phase 3 Final Gate Checklist
Handoff and semantics
 All Phase 2 model inputs are present.
 Partial production is explicitly defined.
 Partial delivery is explicitly defined.
 Production-capacity behavior is defined.
 Material-consumption timing is defined.
 No data-generation rule contradicts Phase 2.
Enterprise and scale
 Synthetic organization is documented.
 Network structure is documented.
 Product and component families are documented.
 Tiny scale is defined.
 Standard scale is defined.
 Stress scale is defined.
 Distribution targets are documented.
Generation
 Generator uses explicit seeds.
 Random streams are isolated.
 Stable identifiers are used.
 Stable export ordering is used.
 No network access is required.
 Same inputs produce identical outputs.
 Generated files are never manually corrected.
Master data
 Supplier records are valid.
 Supplier agreements are valid.
 Components have canonical units.
 Products have active BOMs.
 BOM intervals do not overlap.
 Warehouses and facilities are valid.
 Transfer lanes are valid.
 Customer SLA rules are valid.
Operational data
 Customer demand drives production.
 Production drives material requirements.
 Material requirements drive procurement.
 Inventory transactions reconcile.
 Purchase-order quantities reconcile.
 Production quantities reconcile.
 Customer allocations reconcile.
Temporal data
 Historical period is complete.
 Effective intervals are valid.
 Event time and ingestion time are distinct.
 Late-arriving data tests exist.
 Scenario replay prevents future leakage.
 Snapshots reconcile with transactions.
Evidence documents
 Corpus is original.
 Metadata is complete.
 Effective dates are present.
 Expired-document fixtures exist.
 Unauthorized-document fixtures exist.
 Prompt-injection fixtures exist.
 Expected answers do not leak into documents.
 Retrieval relevance labels exist.
Golden scenario
 Corrected Chennai inventory is used.
 Baseline is calculated.
 Do-nothing result is calculated.
 Transfer candidate is calculated.
 Alternate-supplier candidate is calculated.
 Hybrid candidate is calculated.
 Exact scheduling boundaries are frozen.
 Inventory conservation passes.
 Capacity conservation passes.
 Two reviewers agree.
 Golden JSON outputs are frozen.
Benchmark suite
 Sixty scenarios exist.
 Difficulty levels are assigned.
 Development partition exists.
 Validation partition exists.
 Test partition exists.
 Adversarial partition exists.
 No scenario appears in incompatible partitions.
 Multiple valid answers are represented correctly.
 No test-answer leakage exists.
Ground truth
 Oracle is separate from application code.
 Intermediate calculations are emitted.
 Decimal arithmetic is used.
 Stable tie-breaking is used.
 Every expected result has provenance.
 Every expected recommendation is feasible.
 All frozen scenarios have expected outcomes.
Validation
 Schema errors are zero.
 Referential errors are zero.
 Domain errors are zero.
 Conservation errors are zero.
 Temporal errors are zero.
 Undocumented warnings are zero.
 Dataset statistics are generated.
 Distribution deviations are within tolerance.
Privacy and release
 Dataset is fully synthetic.
 No personal data exists.
 No confidential enterprise data exists.
 No copied incident reports exist.
 Dataset card is complete.
 Manifest is present.
 Checksums are present.
 Clean reproducibility drill passes.
 Dataset version is frozen.
 Phase 3 score is at least 95.
 No automatic-failure condition remains.
