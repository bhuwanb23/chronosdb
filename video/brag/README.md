# ChronosDB × brag — Launch Video Setup

## What is brag?
`brag` is an agent skill that turns your project into a short, shareable launch video — music, motion, and share copy included. One command, powered by Hyperframes.

- Repo: https://github.com/latent-spaces/brag
- Site: https://latent-spaces.github.io/brag/
- No-setup option: https://letsbrag.app (paste site link → 20s video)

## Two Modes

### Mode 1: `/brag-slim` (Recommended for Opus 5.5)
Lean, no Hyperframes, no bundled assets. Model builds story, visuals, music, SFX, mix, render with tools on your machine.

```bash
# Install just brag-slim
npx skills add https://github.com/latent-spaces/brag --skill brag-slim

# Then in Claude Code / Opus 5.5:
# "let's /brag about this"
# or: /brag-slim
```

On Opus 5.5, `/brag` auto-switches to `/brag-slim`. Use `/brag --full` for classic Hyperframes workflow.

### Mode 2: `/brag` (Full Hyperframes)
Bundled assets, Hyperframes rendering (needs GPU).

```bash
# Install full brag plugin
claude plugin install brag
# or
npx skills add https://github.com/latent-spaces/brag --skill brag
```

## ChronosDB Video Brief

Use `video/brag/chronosdb-brief.md` as the project brief when running `/brag`.

**Key inputs brag will use:**
- `docs/screenshots/war_room_main.png` — hero visual
- `docs/diagrams/decision_flow.png` — story arc
- `docs/diagrams/system_architecture.png` — architecture
- `docs/diagrams/db2_architecture.png` — Db2 differentiation
- `docs/diagrams/benchmark_comparison.png` — proof
- `docs/demo/final-script.md` — 2:45 script (use first 20s for brag launch video)
- `docs/demo/caption-file.srt` — captions

**brag output:**
- `assets/demo/demo-video.mp4` (20s launch video for letsbrag.app style, or 2:45 full demo)
- Share copy in `video/brag/share-copy.md`
- Thumbnail in `assets/demo/thumbnails/`

## GPU Rendering (User's Machine)

You have a GPU — render locally:

```bash
# 1. Install brag-slim (no GPU needed for slim, GPU helps for Hyperframes full)
npx skills add https://github.com/latent-spaces/brag --skill brag-slim

# 2. Run brag on ChronosDB
# In Claude Code:
# "let's /brag about this — use video/brag/chronosdb-brief.md"

# 3. Or full Hyperframes (GPU accelerated):
/brag --full

# 4. Output goes to:
# assets/demo/demo-video.mp4
# video/brag/output/
```

## letsbrag.app (No Setup)
1. Deploy ChronosDB docs site (or use GitHub Pages from `docs/`)
2. Paste site link at https://letsbrag.app
3. Get 20-second launch video with music, motion, share copy
4. Download and place in `assets/demo/demo-video.mp4`

## File Map
```
video/brag/
├── README.md                  ← you are here
├── chronosdb-brief.md         ← project brief for /brag agent
├── brag-config.yaml           ← brag configuration
├── share-copy.md              ← social share copy (X, LinkedIn, GitHub)
├── music-brief.md             ← soundtrack brief
└── output/                    ← brag renders here
assets/demo/
├── demo-video.mp4             ← final video (rendered on your GPU)
├── thumbnails/                ← YouTube / GitHub thumbnails
├── screenshots/               ← 10 War Room screenshots
├── architecture-diagrams/     ← 9 diagrams
├── benchmark-charts/          ← benchmark visuals
└── db2-diagrams/              ← Db2 differentiation
```

## Requirements
- Node.js 18+ (for npx skills)
- Claude Code with Opus 5.5 (for brag-slim) OR Hyperframes + GPU (for full)
- ffmpeg (for video post-processing)
- 10GB disk for renders

## Phase 17 Status: Setup ready. Render pending (your GPU). Video not yet produced.
