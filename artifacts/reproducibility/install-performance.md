# Phase 15P: Installation Benchmarking

Measured on the local workspace (Windows, Python 3.13, Node 24). Docker and Db2
operations are not included because those runtimes are unavailable here.

| Operation | Target | Median | P95 | Maximum |
|-----------|--------|--------|-----|---------|
| Setup (Python deps only) | <15 min | <1 min | <1 min | <1 min |
| Seed validation | <5 min | <1 s | <1 s | <1 s |
| Embedding fallback build | <5 min | <5 s | <5 s | <5 s |
| Test suite | n/a | ~75 s | ~90 s | ~120 s |
| Demo ready (Docker/Db2) | <20 min | not measured | not measured | not measured |

The Docker/Db2 row must be re-measured on a host with Docker Engine and the
pinned Db2 image.
