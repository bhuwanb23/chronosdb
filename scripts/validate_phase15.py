#!/usr/bin/env python3
"""Phase 15N: validate the reproducibility contract without manual Db2 steps."""

from __future__ import annotations

import json
import os
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

REQUIRED_FILES = [
    "Makefile",
    "docker-compose.yml",
    ".env.example",
    "config.yaml",
    "requirements.txt",
    "requirements-lock.txt",
    "package-lock.json",
    "README.md",
    "docs/reproducibility/phase-14-handoff-review.md",
    "docs/reproducibility/reproducibility-architecture.md",
    "docs/reproducibility/version-matrix.md",
    "docs/reproducibility/health-checks.md",
    "docs/reproducibility/troubleshooting.md",
    "docs/reproducibility/install-test-report.md",
    "docs/reproducibility/phase-15-completion-report.md",
    "scripts/setup.sh",
    "scripts/db_up.sh",
    "scripts/db_check.sh",
    "scripts/migrate.sh",
    "scripts/seed.py",
    "scripts/build_embeddings.py",
    "scripts/health_check.py",
    "scripts/run_demo.sh",
    "sql/migrations/001_schema.sql",
    "sql/migrations/002_indexes.sql",
    "sql/migrations/003_permissions.sql",
    "sql/migrations/004_vectors.sql",
    "docker/backend/Dockerfile",
    "docker/frontend/Dockerfile",
]

SEED_FILES = [
    "suppliers.sql",
    "components.sql",
    "inventory.sql",
    "orders.sql",
    "customer_orders.sql",
    "production_orders.sql",
    "scenarios.sql",
    "historical_incidents.sql",
    "policies.sql",
    "sops.sql",
]

REQUIRED_TARGETS = [
    "setup",
    "db-up",
    "db-check",
    "migrate",
    "seed",
    "validate-seed",
    "embeddings",
    "embedding-check",
    "backend",
    "frontend",
    "app",
    "benchmark",
    "test",
    "demo",
    "clean",
]


def check_files() -> list[str]:
    issues = [f"missing: {path}" for path in REQUIRED_FILES if not (ROOT / path).exists()]
    issues += [
        f"missing seed: sql/seeds/{name}"
        for name in SEED_FILES
        if not (ROOT / "sql" / "seeds" / name).exists()
    ]
    return issues


def check_makefile() -> list[str]:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    return [f"Makefile target missing: {name}" for name in REQUIRED_TARGETS if not re.search(rf"^{re.escape(name)}:", text, re.M)]


def check_env() -> list[str]:
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    issues = []
    for key in ("DB2_HOST", "DB2_PORT", "DB2_DATABASE", "DB2_USERNAME", "DB2_PASSWORD", "EMBEDDING_MODEL"):
        if not re.search(rf"^{key}=", text, re.M):
            issues.append(f".env.example missing key: {key}")
    if "```" in text:
        issues.append(".env.example must be a plain env file, not Markdown")
    return issues


def check_requirements() -> list[str]:
    text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    issues = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "latest" in line.lower():
            issues.append(f"floating dependency: {line}")
        if "==" not in line:
            issues.append(f"dependency is not pinned: {line}")
    return issues


def check_compose() -> list[str]:
    try:
        import yaml
    except ImportError:
        return ["PyYAML is required to validate docker-compose.yml"]
    issues: list[str] = []
    payload = json.loads(json.dumps(yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))))
    services = payload.get("services", {})
    for name in ("db2", "backend", "frontend"):
        if name not in services:
            issues.append(f"docker-compose service missing: {name}")
    for name in ("backend", "frontend"):
        build = services.get(name, {}).get("build", {})
        dockerfile = build.get("dockerfile") if isinstance(build, dict) else None
        if not dockerfile or not (ROOT / dockerfile).exists():
            issues.append(f"docker-compose {name} Dockerfile missing")
    return issues


def check_health_routes() -> list[str]:
    try:
        from fastapi.testclient import TestClient
        from backend.chronosdb.api.app import app
    except Exception as exc:  # pragma: no cover - environment-specific
        return [f"cannot import API app: {exc}"]

    issues = []
    client = TestClient(app)
    for path in ("/health", "/readiness"):
        response = client.get(path)
        payload = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        if response.status_code != 200 or payload.get("status") != "READY":
            issues.append(f"{path} did not return READY")
    return issues


def check_scripts() -> list[str]:
    issues: list[str] = []
    seed = subprocess.run(
        [sys.executable, "scripts/seed.py", "--validate-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if seed.returncode != 0:
        issues.append("scripts/seed.py --validate-only failed: " + seed.stderr.strip())
    embeddings = subprocess.run(
        [sys.executable, "scripts/build_embeddings.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if embeddings.returncode != 0:
        issues.append("scripts/build_embeddings.py --check failed: " + embeddings.stdout.strip())
    return issues


def check_artifacts() -> list[str]:
    benchmark = ROOT / "benchmark" / "reports" / "benchmark_results.json"
    if not benchmark.exists():
        return ["benchmark/reports/benchmark_results.json is missing"]
    return []


def main() -> int:
    checks = {
        "required_files": check_files(),
        "makefile": check_makefile(),
        "environment": check_env(),
        "dependencies": check_requirements(),
        "docker_compose": check_compose(),
        "health_routes": check_health_routes(),
        "scripts": check_scripts(),
        "benchmark_artifacts": check_artifacts(),
    }
    failed = {name: issues for name, issues in checks.items() if issues}
    report: dict[str, Any] = {
        "report_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "FAIL",
        "checks": {name: ("PASS" if not issues else "FAIL") for name, issues in checks.items()},
        "issues": failed,
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "node": os.environ.get("NODE_VERSION", "not-captured"),
        },
    }
    output = ROOT / "artifacts" / "reproducibility"
    output.mkdir(parents=True, exist_ok=True)
    (output / "validation-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": report["status"], "checks": report["checks"], "issues": failed}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
