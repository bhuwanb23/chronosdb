#!/usr/bin/env bash
# Phase 15F: start a local Db2 instance through Docker Compose.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required for the default Db2 provisioning mode." >&2
  echo "Install Docker Desktop/Engine or follow docs/reproducibility/troubleshooting.md for the local fallback." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "docker compose v2 is required (docker compose, not docker-compose)." >&2
  exit 1
fi

echo "Starting Db2 via Docker Compose..."
docker compose up -d db2

echo "Waiting for Db2 to accept connections..."
for attempt in $(seq 1 60); do
  if docker compose exec -T db2 bash -lc 'db2 connect to "$DBNAME" >/dev/null 2>&1' >/dev/null 2>&1; then
    echo "Db2 is ready."
    exit 0
  fi
  sleep 5
done

echo "Db2 did not become ready in time. Inspect: docker compose logs db2" >&2
exit 1
