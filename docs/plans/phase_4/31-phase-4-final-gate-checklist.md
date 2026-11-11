31. Phase 4 Final Gate Checklist
Release intake
 Phase 3 generator is available.
 Ground-truth oracle is available.
 Domain-model version is frozen.
 Generator version is frozen.
 Dataset seed is frozen.
 No Phase 3 blocking defects remain.
Master data
 All suppliers are synthetic.
 Components have valid units.
 Agreements have valid effective intervals.
 Products have valid BOMs.
 Warehouses and facilities exist.
 Transfer lanes are valid.
 Customers have active SLA policies.
Procurement
 Purchase orders reference valid suppliers and components.
 Received quantity does not exceed ordered quantity.
 Supplier capacity is respected.
 Arrival timestamps are valid.
 Historical status changes are coherent.
Inventory
 Opening balances exist.
 Ledger transactions reconcile.
 Snapshots match the ledger.
 Reservations are not counted twice.
 Transfers have valid dispatch and receipt states.
 Safety-stock logic is valid.
 Golden transferable quantity equals 400.
Production
 Production orders use valid products and facilities.
 Material requirements match BOMs.
 Batch sizes are valid.
 Facility capacity is respected.
 Completed quantity does not exceed planned quantity.
 Material is not consumed before availability.
Customer demand
 Customer orders reference valid customers.
 Order lines reference valid products.
 Allocations reference valid production orders.
 Promised dates are valid.
 Line revenue reconciles.
 Partial fulfilment is represented correctly.
 Revenue at risk uses late quantity only.
Temporal history
 All relevant records include time semantics.
 Effective intervals are half-open.
 No future knowledge leaks into earlier scenarios.
 Late-arriving corrections are represented.
 Historical replay expectations are present.
 Snapshot reconstruction tests pass.
Disruptions and interventions
 Golden outage affects only intended supply.
 Received quantity remains unaffected.
 Recovery lag is applied once.
 Transfer feasibility is correct.
 Alternate-supplier approval is correct.
 Expedition limitations are realistic.
 Rescheduling externalities are represented.
 Hybrid cost equals ₹132,000.
 Infeasible candidates have explicit reasons.
Evidence
 Corpus contains approximately 175 documents.
 All documents are original and synthetic.
 Metadata is complete.
 Effective dates are present.
 Access labels are present.
 Retrieval relevance labels are present.
 Expired-document cases exist.
 Unauthorized-document cases exist.
 Prompt-injection cases exist.
 Expected answers are absent from documents.
Golden scenario
 Exact source records are frozen.
 Exact timeline is frozen.
 Do-nothing result is verified.
 Every candidate is verified.
 Expected recommendation is feasible.
 Budget is respected.
 Causal traces are complete.
 Provenance is complete.
 Two independent reviewers agree.
 Golden output hashes are recorded.
Benchmark
 Sixty scenarios exist.
 Partition manifest is frozen.
 Exclusive partitions do not overlap.
 Difficulty labels exist.
 All expected outcomes exist.
 Multiple valid optima are represented.
 No-feasible-plan scenarios exist.
 Insufficient-data scenarios exist.
 Temporal scenarios exist.
 Partial-fulfilment scenarios exist.
Validation
 File-validation errors are zero.
 Type-validation errors are zero.
 Referential errors are zero.
 Temporal errors are zero.
 Inventory-conservation errors are zero.
 Capacity errors are zero.
 Financial errors are zero.
 Benchmark errors are zero.
 Undocumented warnings are zero.
Governance
 Private data findings are zero.
 Secret findings are zero.
 Licensing review passes.
 Test-answer leakage is zero.
 Partition leakage is zero.
 Dataset card is complete.
Reproducibility and release
 Ten golden runs produce identical results.
 Clean-room generation succeeds.
 Deterministic checksums match.
 Load-order manifest exists.
 Release manifest exists.
 Release notes exist.
 Dataset version is 1.0.0.
 Phase 4 score is at least 95.
 No automatic-failure condition remains.
