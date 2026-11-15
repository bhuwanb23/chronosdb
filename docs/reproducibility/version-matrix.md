# Phase 15C: Environment Definition

## Pinned versions

| Component | Version |
|-----------|---------|
| Python | 3.12.x (supported 3.11–3.13) |
| FastAPI | 0.162.4 |
| Uvicorn | 0.54.0 |
| Pydantic | 2.14.3 |
| ibm-db | 3.3.0 |
| PyYAML | 6.0.3 |
| pytest | 8.4.2 |
| Node.js | 20.x (Docker image `node:20-alpine`) |
| Db2 | `icr.io/db2_community/db2:11.5.9.0` |
| Embedding model | `bge-small-en-v1.5` (deterministic fallback supported) |
| React | 18.2.x |
| Vite | 4.x |

## Environment matrix

| Resource | Minimum |
|----------|---------|
| OS | Linux x86_64 (Ubuntu 22.04 reference) or Windows with WSL2 |
| CPU | 4 cores |
| RAM | 8 GB (16 GB recommended for Db2) |
| Storage | 20 GB free |
| Docker | Docker Engine/Desktop with Compose v2 |

The exact Python pins live in `requirements.txt` and `requirements-lock.txt`.
The frontend lock file is `src/frontend/package-lock.json` (mirrored at the
repository root as `package-lock.json`).
