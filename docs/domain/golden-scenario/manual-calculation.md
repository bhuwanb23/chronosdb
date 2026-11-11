# Golden Scenario Manual Calculation

## 1. No-disruption baseline

Pune has 400 MCU units and `PROD-876` needs 400. The original PO arrival on
13 November supplies the next 800 units before the next two orders need them.

| Order | Start | Complete | Delivery | Promise | Result |
|---|---|---|---|---|---|
| PROD-876 / CO-701 | 12 Nov | 14 Nov | 15 Nov | 15 Nov | On time |
| PROD-882 / CO-704 | 15 Nov | 17 Nov | 18 Nov | 18 Nov | On time |
| PROD-889 / CO-711 | 18 Nov | 20 Nov | 21 Nov | 21 Nov | On time |

Baseline breaches: 0. Baseline revenue at risk: INR 0.

## 2. Do-nothing case

The outage delays `PO-2208` from 13 November to 27 November. `PROD-876`
consumes the 400 Pune units and remains on schedule. The next orders wait for
the delayed receipt and facility capacity:

| Order | Start | Complete | Delivery | Promise | Delay |
|---|---|---|---|---|---:|
| PROD-876 / CO-701 | 12 Nov | 14 Nov | 15 Nov | 15 Nov | 0 days |
| PROD-882 / CO-704 | 27 Nov | 29 Nov | 30 Nov | 18 Nov | 12 days |
| PROD-889 / CO-711 | 29 Nov | 1 Dec | 2 Dec | 21 Nov | 11 days |

Do-nothing result:

- breached customer orders: 2;
- revenue at risk: `200 * 4,000 + 200 * 4,000 = INR 1,600,000`;
- quantity-weighted delay: `(200 * 12) + (200 * 11) = 4,600 unit-days`;
- equivalent quantity-hours: `110,400`.

## 3. Transfer candidate

Chennai transferable quantity is:

```text
700 - 180 - 120 = 400 MCU units
```

Transfer cost is:

```text
40,000 + (400 * 50) = INR 60,000
```

The transfer supports `PROD-882`. `PROD-889` waits for the 27 November receipt:

- breached orders: 1 (`CO-711`);
- revenue at risk: INR 800,000;
- revenue protected: INR 800,000.

## 4. Alternate-supplier candidate

Supplier `S-208` can provide 400 units. Its arrival is 16 November. Premium:

```text
400 * (1,180 - 1,000) = INR 72,000
```

This supports `PROD-882` after material arrives. Under the day-bucket schedule,
`CO-704` delivers 19 November and is one day late; `PROD-889` still waits for
the delayed primary PO.

- breached orders: 2;
- revenue at risk: INR 1,600,000;
- incremental cost: INR 72,000.

## 5. Hybrid candidate

The transfer arrives 13 November and the alternate supply arrives 16 November.
The orders run as follows:

| Order | Start | Complete | Delivery | Promise | Result |
|---|---|---|---|---|---|
| PROD-876 / CO-701 | 12 Nov | 14 Nov | 15 Nov | 15 Nov | On time |
| PROD-882 / CO-704 | 15 Nov | 17 Nov | 18 Nov | 18 Nov | On time |
| PROD-889 / CO-711 | 18 Nov | 20 Nov | 21 Nov | 21 Nov | On time |

Hybrid cost:

```text
INR 60,000 + INR 72,000 = INR 132,000
```

Hybrid result:

- breached orders: 0;
- revenue at risk: INR 0;
- revenue protected versus do nothing: INR 1,600,000;
- budget remaining: INR 68,000.

## Expected recommendation

Under `MINIMIZE_SLA_BREACHES`, the hybrid candidate is recommended. It is
feasible, uses approved supply, stays within budget, protects source safety
stock, and is the only candidate in this set that protects both affected
customer orders.
