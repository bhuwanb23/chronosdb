# ChronosDB visual asset pack

ChronosDB uses a visual language called **Temporal Operations**: a dark
graphite field, a cyan evidence signal, amber decision markers, and coral
failure propagation. Rounded glass panels and a 44px grid make complex system
behavior feel inspectable instead of ornamental.

## Palette

| Token | Hex | Meaning |
| --- | --- | --- |
| Graphite | `#07141E` | System background |
| Signal cyan | `#6EF3FF` | Evidence, active state, database |
| Decision amber | `#FFC857` | Intervention, timing, warning |
| Risk coral | `#FF6B6B` | Disruption, exposure, SLA risk |
| Verified lime | `#B8F16B` | Selected, feasible, verified |
| Muted blue | `#91B4C0` | Supporting text |

## Files

Every visual has an editable `.svg` source and a matching `.png` export.

- `logo-mark` — primary orbit/database mark
- `logo-lockup` — horizontal brand lockup
- `favicon` — compact mark
- `hero-time-machine` — landing page or pitch cover
- `operations-war-room` — dashboard concept
- `cascade-anatomy` — supplier-to-customer impact chain
- `controlled-intelligence` — AI authority architecture
- `decision-replay` — temporal replay concept
- `evidence-contract` — claim-to-source trace
- `db2-backbone` — Db2 role map
- `counterfactual-board` — intervention comparison
- `supply-chain-signal-map` — network propagation visual
- `trust-boundary` — model versus truth boundary
- `decision-loop` — end-to-end user workflow
- `signal-grid` — decorative background / section visual
- `social-card` — 1200×630 social or presentation card

## Regenerate

From the repository root:

```powershell
python scripts\generate_assets.py
python scripts\export_asset_pngs.py
```

The SVG generator has no project runtime dependencies. PNG export uses a
locally installed Chrome or Edge headless renderer and is intentionally kept
outside the application dependency list.
