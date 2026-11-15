# Phase 15O: Troubleshooting Guide

## Db2 does not start

1. Check Docker: `docker ps`
2. Inspect logs: `docker compose logs db2`
3. Restart: `docker compose restart db2`
4. Confirm port 50000 is free: `docker compose port db2 50000`

The Db2 container needs `LICENSE=accept` and a strong `DB2_PASSWORD`.

## Migration fails

1. Confirm Db2 is healthy: `make db-check`
2. Run migrations one at a time with `DRY_RUN=0 bash scripts/migrate.sh`
3. Role creation in `003_permissions.sql` requires SECADM; grant it to the
   migration user or skip that migration in restricted environments.

## Seed failure

1. Validate files without a database: `make validate-seed`
2. Confirm `db2` CLI is on PATH or use the Docker-backed migration shell.
3. Inspect the failing file under `sql/seeds/` and the first error from `db2`.

## Embedding creation failure

1. Run `python scripts/build_embeddings.py` to regenerate the deterministic
   fallback.
2. Validate with `make embedding-check`.
3. If a local model is required, install it separately; the fallback is the
   supported reproducible path.

## Missing environment variables

1. `cp .env.example .env`
2. Replace every `change-me` value.
3. Re-run `make setup` or restart `make app`.

## Port collision

1. Check the port: `docker compose ps`
2. Change `DB2_PORT`, backend `8000`, or frontend `3000` in `.env` /
   `docker-compose.yml`.
3. Restart: `docker compose up -d --build`

## Health check fails

1. `curl http://localhost:8000/health`
2. `curl http://localhost:8000/readiness`
3. `docker compose logs backend`
4. Re-run `make health`.
