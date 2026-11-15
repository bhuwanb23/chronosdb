# Phase 15N: Installation Test Report

## Scope

This report records the reproducibility checks that can be executed without a
privileged Db2 host. Container and Db2-dependent steps are validated statically
and by the health contract; they are marked separately below.

## Checks

| Check | Command | Result |
|-------|---------|--------|
| Dependency pins | `python scripts/validate_phase15.py` | PASS |
| Makefile targets | `python scripts/validate_phase15.py` | PASS |
| Docker Compose shape | `python scripts/validate_phase15.py` | PASS |
| Seed/embedding fixtures | `python scripts/validate_phase15.py` | PASS |
| API health routes | `python scripts/validate_phase15.py` | PASS |
| Benchmark artifact | `python benchmark/runners/benchmark_runner.py` | PASS |
| Full test suite | `python -m pytest tests -q` | PASS |

## Environment A/B/C

The same commands are used for a fresh machine, fresh VM, and Docker host:

```bash
make setup
make demo
```

`make demo` starts Db2, applies migrations, loads seeds, prepares the
deterministic embedding fallback, starts the application, and verifies health.
Docker and Db2 execution must be performed on a host with Docker Engine and
network access to the pinned `icr.io/db2_community/db2:11.5.9.0` image.

## Known limitation

This workspace does not provide Docker or a Db2 server, so the container startup
and live Db2 migration were not executed here. The static contract, scripts,
and API health routes were validated.
