# Golden Scenario Definition

## Identity

- Scenario ID: `SC-GOLD-001`
- Organization: synthetic electronics manufacturer
- As-of time: `2026-11-11T02:30:00Z` (`08:00 Asia/Kolkata`)
- Horizon: 30 calendar days
- Objective: `MINIMIZE_SLA_BREACHES`
- Budget: INR 200,000
- Approved suppliers only: yes
- Minimum source safety stock: enforced

## Disruption

Supplier `S-104` is unavailable for 14 days:

- start: `2026-11-11T02:30:00Z`;
- end: `2026-11-25T02:30:00Z`;
- recovery lag: 2 calendar days;
- effective new arrival for `PO-2208`: `2026-11-27T02:30:00Z`;
- scope: `ALL_SUPPLY`.

## Corrected baseline decision

The corrected scenario uses Chennai on-hand inventory of 700 MCU units.
After 180 units of committed local demand and 120 units of safety stock:

```text
transferable = 700 - 180 - 120 = 400 MCU units
```

The earlier 500-unit value would allow only 200 transferable units and cannot
support the selected full-transfer/hybrid ground truth. It is rejected and must
not appear in expected outputs.

## Objective

The expected recommendation is the hybrid intervention: transfer 400 MCU
units from Chennai and order 400 MCU units from approved supplier `S-208`.
