# Verified Golden Figures (SCN-GOLD-001)

These are the only numbers the demo may show. Each row cites the frozen engine artifact it came from.

Sources (public repo, `main`):
- A: `artifacts/phase-5/golden-impact-result.json`, `artifacts/phase-5-handoff/benchmark-summary.json`
- B: `data/releases/v1.0.0/golden/expected_candidate_results.json`
- C: `data/golden/expected_recommendation.json`
- D: `artifacts/phase-5-handoff/determinism-report.json`

## Impact (Phase 5 Do-Nothing)
| Figure | Value | Source |
|---|---|---|
| Revenue at risk | ₹16,00,000 (INR 1,600,000) | A: headline_metrics.revenue_at_risk |
| SLA-breached customer orders | 2 (CO-0704, CO-0711) | A: sla_breached_customer_order_count |
| Affected production orders | 2 (MO-0882, MO-0889) | A |
| Affected purchase orders | 1 (PO-2208) | A |
| Affected supplier | SUP-0104 | A |
| Affected component | CMP-MCU-42 | A |
| Max delay | 288 hours | B: DO-NOTHING maximum_delay |
| Shortage | 4 shortage records on CMP-MCU-42, 200 units each | A: shortages |
| Financial fidelity | 1.0 | A: benchmark-summary golden |
| Determinism | repeated hashes identical | D |

## Candidate interventions (B)
| Candidate | Feasible | Cost | Revenue protected | SLA breaches | Delay (h) |
|---|---|---|---|---|---|
| DO-NOTHING | yes | ₹0 | ₹0 | 2 | 288 |
| INT-GOLD-A | yes | ₹60,000 | ₹8,00,000 | 1 | 264 |
| INT-GOLD-B | yes | ₹72,000 | ₹0 | 2 | 264 |
| **INT-GOLD-C (recommended)** | yes | **₹1,32,000** | **₹16,00,000** | **0** | **0** |
| INT-GOLD-RESCHEDULE | yes | ₹60,000 | ₹8,00,000 | 1 | 264 |
| INT-GOLD-EXPEDITE | **no** (COMPLETE_SUPPLIER_OUTAGE) | — | — | — | — |
| INT-GOLD-TRANSFER-500 | **no** (SOURCE_SAFETY_STOCK_VIOLATION) | — | — | — | — |

## Recommendation (C)
- Recommended: INT-GOLD-C. Objective: MINIMIZE_SLA_BREACHES. Hard constraints satisfied: true.
- Budget: ₹1,32,000 is under the ₹2 lakh limit. ✅
- Net protected value (C): ₹14,68,000.

## Not verified — must NOT appear in demo until sourced
- Utility scores (0.91, 0.78, etc.), confidence 96%
- Recall@5 0.87, MRR 0.82 (retrieval metrics were not found in the artifacts reviewed)
- "5 evidence sources" (each candidate lists 3 document references)
- "306 orders", "42 SLA breaches", "₹15.2M", "₹8.4M", "₹2.1M" (these were typed into mockups, not produced by the engine)
- Action composition of INT-GOLD-C ("INT-GOLD-C (action mix not yet verified)") — not exposed in the public data reviewed
- Injection blocked 100%, prompt-injection 0%, replay accuracy 100% — not re-verified in this phase
