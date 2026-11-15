# Phase 18G: Demo Video Compliance

| Check | Result |
|---|---|
| Video file exists (`assets/demo/demo-video.mp4`) | ❌ NOT PRESENT |
| Length 2–3 min (target 2:45) | ⏸ cannot verify |
| Captions (`docs/demo/caption-file.srt`) | ✅ 7 segments, 0:00–3:00 (timing not verified against audio) |
| Audio clear | ⏸ |
| Public URL | ❌ no video uploaded |
| Incognito / no-login playback | ⏸ |

Blocker: the video must be rendered on the user's GPU using `video/brag/`, then uploaded to a public host (YouTube unlisted/public, or the repo's Releases). Then re-run this review.

Also pending: the Phase 17 golden-scenario conflict (budget and magnitudes) must be resolved before the video is recorded.

## Result: ❌ FAIL (video missing)
