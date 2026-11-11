# Phase 2U: Domain Review Report

## Review result

The A–O model was reviewed from supply-chain, manufacturing, financial,
temporal, and causal perspectives. The corrected golden scenario was used as
the reference case.

## Supply-chain review

- Supplier approval and capacity are explicit.
- Received and cancelled quantities are protected.
- Delayed outstanding receipts are deterministic.
- Transfers cannot violate source safety stock or committed demand.
- No intervention creates material from nothing.

Result: **Pass**.

## Manufacturing review

- Mandatory materials are required before production.
- Facility capacity and deterministic priority are considered.
- Completed output is preserved.
- Rescheduling must report both helped and harmed orders.
- Day-bucket scheduling is labelled as an MVP simplification.

Result: **Pass with simplification recorded**.

## Financial review

- Revenue at risk uses late quantity, not full order value by default.
- Incremental alternate-supplier premium is separated from base procurement.
- Transfer, expedite, and rescheduling costs have explicit owners.
- All golden values use INR.

Result: **Pass**.

## Temporal review

- Event, reported, ingestion, effective, as-of, and horizon times are distinct.
- Effective intervals are half-open.
- Late-arriving data cannot mutate a completed scenario.
- UTC is canonical and Asia/Kolkata is the display zone.

Result: **Pass**.

## Causal review

- Every customer impact traces through intermediate supply, inventory,
  production, and fulfilment states.
- Contextual evidence cannot create operational facts.
- Necessary constraints and contributing factors are distinct.
- Direct outage-to-revenue jumps are prohibited.

Result: **Pass**.

## Golden-scenario independent calculation

Calculation A used the event timeline and production order sequence in
`manual-calculation.md`. Calculation B independently applied:

1. 400 Pune MCU units to `PROD-876`;
2. 400 Chennai transfer units to `PROD-882`;
3. 400 alternate-supplier units to `PROD-889`;
4. 100 finished units/day capacity and one-day delivery;
5. promised-date comparisons per customer line.

Both calculations agree:

- do-nothing breached orders: 2;
- do-nothing revenue at risk: INR 1,600,000;
- hybrid intervention cost: INR 132,000;
- hybrid breached orders: 0;
- hybrid revenue protected: INR 1,600,000;
- recommendation: `INT-HYBRID-400`.

## Remaining limitations

The review is specification-level. Executable domain tests, generated data,
Db2 queries, and simulator behavior belong to later phases.
