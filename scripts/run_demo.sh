#!/usr/bin/env bash
# Phase 15J/15K: verify the demo is healthy and print evaluator-facing URLs.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python
fi

echo "Checking ChronosDB health..."
"$PYTHON" scripts/health_check.py --base-url "${CHRONOSDB_BACKEND_URL:-http://localhost:8000}" --retries 30

cat <<'MSG'
========================================
ChronosDB Demo Ready
Backend API:  http://localhost:8000
API docs:     http://localhost:8000/docs
Frontend UI:  http://localhost:3000
Golden:       SCN-GOLDEN-001
========================================
MSG
