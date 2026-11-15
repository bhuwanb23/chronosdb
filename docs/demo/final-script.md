# Phase 17F: Demo Script (verified figures only)

Target: 2:45. All numbers come from `docs/demo/verified-golden-figures.md` (SCN-GOLD-001).

## Opening (0:00–0:20) — Pain
Visual: War Room main (KPIs visible).
> "Modern supply chains generate huge amounts of operational data. When a disruption hits, most systems can only say that something went wrong. They cannot show what fails next, compare recovery options, or prove which one to trust."

## Disruption (0:20–0:45) — Enter the case
Visual: Executive dashboard, supplier SUP-0104.
> "Supplier SUP-0104 is down. Our recovery budget is under two lakh rupees. Let's run the counterfactual analysis."

## Impact cascade (0:45–1:15) — Consequences
Visual: Dependency cascade.
> "ChronosDB computes every impact with deterministic supply-chain logic, not a language-model guess. The outage reaches component CMP-MCU-42, two production orders, and two customer orders. Revenue at risk is sixteen lakh rupees, and two SLA breaches are at stake."

On-screen: ₹16,00,000 at risk • 2 customer orders • 2 SLA breaches

## Candidate futures (1:15–1:50) — Decision
Visual: Intervention comparison.
> "ChronosDB evaluates seven candidate actions and keeps only the feasible ones. Two options are infeasible: an expedite is blocked by a complete supplier outage, and a transfer breaks a safety-stock rule. Of the feasible plans, INT-GOLD-C costs one lakh thirty-two thousand rupees, protects sixteen lakh rupees, and leaves zero SLA breaches."

On-screen: ★ INT-GOLD-C • ₹1,32,000 • ₹16,00,000 protected • 0 breaches

## Evidence (1:50–2:20) — Proof
Visual: Evidence explorer.
> "Every candidate links to supporting records in Db2: supplier notices, procedures, and incident reports."

## Replay (2:20–2:45) — Trust
Visual: Timeline replay and audit explorer.
> "Run the golden scenario again and you get the same hashes. The decision can be replayed and audited step by step."

## Closing (2:45–3:00)
> "ChronosDB doesn't ask you to trust an AI recommendation. It lets you replay, verify, and audit every decision. ChronosDB is the Db2 time machine for enterprise decisions."
