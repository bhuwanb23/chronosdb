# Golden Scenario Causal Traces

## CO-704 in the do-nothing run

```text
S-104 outage
 -> PO-2208 receipt moves from 13 Nov to 27 Nov
 -> C-MCU-42 balance reaches zero after PROD-876
 -> PROD-882 cannot start until 27 Nov
 -> PROD-882 completes 29 Nov
 -> CO-704 delivers 30 Nov
 -> promised date 18 Nov is breached
 -> 200 late products * INR 4,000 = INR 800,000 at risk
```

## CO-711 in the do-nothing run

```text
S-104 outage
 -> PO-2208 receipt moves from 13 Nov to 27 Nov
 -> PROD-889 waits behind PROD-882 for material and capacity
 -> PROD-889 completes 1 Dec
 -> CO-711 delivers 2 Dec
 -> promised date 21 Nov is breached
 -> 200 late products * INR 4,000 = INR 800,000 at risk
```

## CO-704 and CO-711 in the hybrid run

```text
WH-CHENNAI transfer of 400 MCU -> arrives 13 Nov -> supports PROD-882
S-208 alternate supply of 400 MCU -> arrives 16 Nov -> supports PROD-889
 -> both orders complete on planned schedule
 -> both customer lines deliver on promised dates
 -> revenue at risk is INR 0
```

Each trace is scoped to `SC-GOLD-001`, a simulation run, `phase-2-v1`, and the
source records in `input-records.csv`.
