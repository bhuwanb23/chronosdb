#!/usr/bin/env python3
"""Phase 15M: verify ChronosDB backend health and readiness."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any


def fetch(base_url: str, path: str, timeout: float) -> dict[str, Any]:
    url = base_url.rstrip("/") + path
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def check(base_url: str, timeout: float, retries: int) -> dict[str, Any]:
    last_error = None
    for attempt in range(retries + 1):
        try:
            health = fetch(base_url, "/health", timeout)
            readiness = fetch(base_url, "/readiness", timeout)
            return {"health": health, "readiness": readiness}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = str(exc)
            if attempt < retries:
                time.sleep(2)
    return {"error": last_error}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = check(args.base_url, args.timeout, args.retries)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Health: {result.get('health', result)}")
        print(f"Readiness: {result.get('readiness', result)}")

    health = result.get("health", {})
    readiness = result.get("readiness", {})
    ok = (
        health.get("status") == "READY"
        and readiness.get("status") == "READY"
    )
    if ok:
        print("Health verification passed.")
        return 0
    print("Health verification failed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
