# Phase 17E: Golden Demo Scenario (SCN-GOLD-001)

All values are verified against the frozen engine artifacts. See `verified-golden-figures.md` for sources.

## Disruption
- Supplier SUP-0104, component CMP-MCU-42
- Recovery budget: under ₹2 lakh

## Impact (Do-Nothing)
- Revenue at risk: ₹16,00,000
- SLA-breached customer orders: 2 (CO-0704, CO-0711)
- Production orders affected: 2 (MO-0882, MO-0889)
- Purchase order affected: PO-2208
- Max delay: 288 hours

## Recommendation
- INT-GOLD-C (objective MINIMIZE_SLA_BREACHES, hard constraints satisfied)
- Cost ₹1,32,000 (within budget)
- Revenue protected ₹16,00,000, net ₹14,68,000
- SLA breaches: 0

## Alternatives
- INT-GOLD-A and INT-GOLD-RESCHEDULE: ₹60,000, protect ₹8,00,000, 1 breach
- INT-GOLD-B: ₹72,000, protects nothing, 2 breaches
- INT-GOLD-EXPEDITE: infeasible (complete supplier outage)
- INT-GOLD-TRANSFER-500: infeasible (safety-stock violation)

## Reproducibility
- Repeated runs produce identical hashes (determinism report).
- Financial fidelity 1.0 on the golden benchmark.

## Open items
1. Confirm the action mix of INT-GOLD-C before calling it "Transfer + Expedite + Reschedule" (not present in public data reviewed).
2. Retrieval metrics (Recall@5, MRR) must be re-measured before being shown.
3. Security claims (SQL injection, prompt injection) must be re-verified before being shown.
