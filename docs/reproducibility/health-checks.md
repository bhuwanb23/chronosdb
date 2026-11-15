# Phase 15M: Health Verification

ChronosDB exposes evaluator-facing liveness and readiness endpoints.

| Endpoint | Purpose | Expected body |
|----------|---------|---------------|
| `GET /health` | Process and dependency health | `{"status": "READY", "checks": {...}}` |
| `GET /readiness` | Db2, vectors, audit, simulation readiness | `{"status": "READY", "checks": {...}}` |
| `GET /health/live` | Foundation liveness | `{"status": "alive"}` |
| `GET /health/ready` | Foundation Db2 readiness | `{"status": "ready"}` |
| `GET /api/v1/health` | Phase 11 API health | `{"status": "SUCCESS", ...}` |
| `GET /api/v1/readiness` | Phase 11 API readiness | `{"status": "SUCCESS", ...}` |

## Automated check

```bash
make health
```

The check uses `scripts/health_check.py`, retries for up to 60 seconds, and exits
non-zero unless both `/health` and `/readiness` return `READY`.
