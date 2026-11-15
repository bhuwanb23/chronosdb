#!/usr/bin/env bash
# Phase 15D/15E: install dependencies and create the local configuration.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python
fi

echo "Using $($PYTHON --version)"
if [ ! -d .venv ]; then
  "$PYTHON" -m venv .venv
fi

if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  # shellcheck disable=SC1091
  source .venv/Scripts/activate
fi

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ -f src/frontend/package.json ]; then
  if command -v npm >/dev/null 2>&1; then
    npm ci --prefix src/frontend
  else
    echo "npm not found; skipping frontend dependency install." >&2
  fi
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Change change-me values before production use."
fi

mkdir -p artifacts/reproducibility
echo "Setup complete."
