#!/usr/bin/env bash
# Phase 15F: verify that a Db2 instance is reachable.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if command -v db2 >/dev/null 2>&1; then
  db2 connect to "${DB2_DATABASE:-CHRONOSDB}" user "${DB2_USERNAME:-db2inst1}" using "${DB2_PASSWORD:-change-me}"
  db2 "SELECT CURRENT SERVER, CURRENT TIMESTAMP FROM SYSIBM.SYSDUMMY1"
  db2 connect reset >/dev/null
  exit 0
fi

if command -v docker >/dev/null 2>&1; then
  docker compose exec -T db2 bash -lc 'db2 connect to "$DBNAME" && db2 "SELECT CURRENT SERVER FROM SYSIBM.SYSDUMMY1" && db2 connect reset'
  exit 0
fi

echo "Neither the db2 CLI nor docker compose is available." >&2
exit 1
