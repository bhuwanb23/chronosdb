# Phase 17O: Backup Demo Paths

## Phase 17 Deep Dive: Demo, Storytelling, and Visual Assets

### Critical Rule
**Demo must never fail live.**

### Backup Paths

#### If UI fails:
Use **Pre-recorded Demo** (`assets/demo/demo-video.mp4`)
- Play video, narrate live over it
- Video is 2:45, captions on

#### If Db2 unavailable:
Use **Frozen Screenshots** (`assets/demo/screenshots/`)
- Walk through screenshots in shot-list order
- All screenshots are frozen Golden Scenario outputs

#### If API unavailable:
Use **Replay Video** + Screenshots
- Show `timeline_replay.png` + `audit_explorer.png`
- Explain replay from screenshots

#### If Video fails:
Use **Live War Room** (`make demo`)
- Run Golden Scenario live
- Fall back to screenshots if needed

### Pre-Demo Checklist
- [ ] `make demo` tested (Phase 15)
- [ ] Video file present (`assets/demo/demo-video.mp4`)
- [ ] Screenshots present (`assets/demo/screenshots/`)
- [ ] Captions present (`docs/demo/caption-file.srt`)
- [ ] Offline copy on USB (no network dependency)

### Deliverable Location
`/home/user/chronosdb/docs/demo/backup-demo-plan.md`

## Phase 17O Status: ✅ COMPLETE
