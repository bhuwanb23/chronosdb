# Phase 17 Completion Report

## Summary
The demo package is authored and the brag video setup is ready. The final video render and external judge review are pending.

## Completed
- Story, narrative, golden scenario, 2:45 script, shot list, voice-over, captions (`caption-file.srt`), backup plan.
- Visual assets: 9 architecture diagrams, Db2 depth graphic, 11 War Room screenshots, thumbnail, benchmark charts. All SVG→PNG via `scripts/generate_phase17_assets.py` and `scripts/generate_phase16_assets.py`.
- brag setup in `video/brag/`: project brief, config, music brief, share copy, README with GPU render steps.

## Pending
- Full video render (`assets/demo/demo-video.mp4`) on the user's GPU.
- Launch cut (20 s) render.
- Judge review (17P/17Q). No scores have been recorded.

## Corrections to earlier work
- The earlier draft of `judge-review-results.md` contained simulated pass rates. These were removed.
- Phase 16 documents (`docs/architecture/independent-documentation-review.md`, the Phase 16 audit report) state "95%+ understanding" from reviewers. No real reviewer sessions took place. Treat those figures as unvalidated.

## Resolved: currency and golden figures
- Currency: ₹ only (user instruction).
- Golden figures: the spec values are the engine's real output (₹16,00,000, 2 breaches). The earlier War Room figures (₹15.2M, 306 orders, 42 breaches, 0.91 utility) were typed into the mockups and have been removed from demo materials. See `docs/demo/verified-golden-figures.md`.
- The HYBRID plan cost (₹1,32,000) is under the ₹2 lakh limit.

## Milestone
M6 (Submission Complete) is not yet reached. Phase 17 is not closed.
