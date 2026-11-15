# Phase 15N: Reproducibility Validation

## Automated validation

```bash
python scripts/validate_phase15.py
```

The validator checks required files, Makefile targets, pinned dependencies,
environment keys, Compose services/Dockerfiles, `/health` and `/readiness`
responses, seed fixtures, embedding fallback, and benchmark artifacts. It writes
`artifacts/reproducibility/validation-report.json`.

## Installation test matrix

| Environment | Command | Status |
|-------------|---------|--------|
| A: fresh machine | `make setup && make demo` | Requires Docker/Db2 host |
| B: fresh VM | `make setup && make demo` | Requires Docker/Db2 host |
| C: Docker host | `docker compose up -d --build` | Requires Docker/Db2 host |

## Golden scenario and benchmark

```bash
python benchmark/runners/benchmark_runner.py
python -m pytest tests -q
```

The benchmark runner writes JSON, Markdown, and SQLite reports. The full test
suite covers the golden scenario, replay, recovery, adversarial, load, and
reproducibility paths.

## Current limitation

This workspace has no Docker Engine and no Db2 server. The static contract and
API health routes were validated here; live container startup and Db2 migration
must be re-run on a Docker-capable host.
