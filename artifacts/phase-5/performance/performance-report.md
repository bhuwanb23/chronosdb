# Impact Engine Performance Report

- Result hash: `b087e079b9688aa3ffe1fa83b45a6e9ec4ad0c9490d3f5ea3ba7973482aa246e`
- Platform: `Windows-11-10.0.26200-SP0`
- Python: `3.13.14`

Each scale measures the complete deterministic pipeline plus separately timed domain stages. Results are release-file runs without Db2 latency.

- `tiny` workload `1`: total p95 `58.717 ms`
- `demo` workload `2`: total p95 `103.124 ms`
- `standard` workload `4`: total p95 `163.165 ms`
- `stress` workload `8`: total p95 `241.155 ms`
