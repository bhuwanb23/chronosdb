# ChronosDB — brag Project Brief

**One line:** ChronosDB is the Db2 time machine for enterprise decisions.

**Problem:** Dashboards show that a supply-chain disruption happened. They do not show what fails next, compare recovery options, or prove which recovery to trust.

**What it does:** Takes a supplier outage (SUP-0104, 14 days), computes deterministic impact, simulates 6 futures, selects the best feasible recovery (HYBRID: Transfer + Expedite + Reschedule, utility 0.91, $8.4M protected), attaches Db2-backed evidence, and lets anyone replay the decision.

**Proof points (frozen Golden Scenario SCN-GOLDEN-001):**
- $15.2M revenue at risk, 306 orders, 42 SLA breaches
- Revenue fidelity 100%, deterministic replay 100%
- Recall@5 0.87, MRR 0.82, 0% unsupported claims
- SQL injection 100% blocked
- `make demo` reproduces the golden run on a fresh machine (<20 min)

**Audience:** Hackathon / competition judges and technical reviewers who have 10 seconds of attention.

**Tone:** Confident, plain, outcome-first. No implementation jargon in voice-over.

**Story arc (must hold):** Disruption → Cascade → Alternative Futures → Best Recovery → Evidence → Replay → Trust.

**Hero assets (use these, do not redraw):**
- `docs/screenshots/war_room_main.png` — opening and closing hero
- `docs/screenshots/dependency_cascade.png` — cascade beat
- `docs/screenshots/intervention_comparison.png` — futures beat (HYBRID highlighted)
- `docs/screenshots/evidence_explorer.png` — evidence beat
- `docs/screenshots/timeline_replay.png` and `audit_explorer.png` — replay beat
- `docs/diagrams/decision_flow.png` — story spine
- `docs/diagrams/system_architecture.png` — architecture beat
- `assets/demo/db2-depth-graphic.png` — "Why Db2?" beat
- `docs/screenshots/benchmark_results.png` — proof beat

**Voice-over source:** `docs/demo/final-script.md` (≈420 words, target 140–160 wpm).
**Captions:** `docs/demo/caption-file.srt`.

**Length targets:**
- Full video: 2:45 (hard max 3:00)
- Launch cut: 20 seconds (letsbrag.app style), built from the opening, intervention, and closing beats

**Must not change:** golden scenario values, metric values, the memorable line "ChronosDB is the Db2 time machine for enterprise decisions."

**Must include on screen:** captions, readable text (no dashboard text smaller than legible at 1080p), Db2 named explicitly, evidence and replay shown.

**Output:**
- `assets/demo/demo-video.mp4` (full 2:45)
- `video/brag/output/launch-20s.mp4` (launch cut)
- `assets/demo/thumbnails/thumbnail-16x9.png` (thumbnail)
- `video/brag/share-copy.md`
