#!/usr/bin/env bash
# Phase 15G: apply all SQL migrations in lexical order.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATIONS_DIR="$ROOT/sql/migrations"
cd "$ROOT"

shopt -s nullglob
migrations=("$MIGRATIONS_DIR"/*.sql)
if [ ${#migrations[@]} -eq 0 ]; then
  echo "No migrations found in $MIGRATIONS_DIR" >&2
  exit 1
fi

run_sql() {
  local file="$1"
  if [ "${DRY_RUN:-0}" = "1" ]; then
    echo "[dry-run] db2 -tvf $file"
    return 0
  fi
  if command -v db2 >/dev/null 2>&1; then
    db2 -tvf "$file"
    return 0
  fi
  if command -v docker >/dev/null 2>&1; then
    docker compose exec -T db2 bash -lc "db2 -tvf '/sql/migrations/$(basename "$file")'"
    return 0
  fi
  echo "db2 CLI or docker compose is required to apply migrations." >&2
  return 1
}

for migration in "${migrations[@]}"; do
  echo "Applying $(basename "$migration")"
  run_sql "$migration"
done

echo "Schema migration complete."
