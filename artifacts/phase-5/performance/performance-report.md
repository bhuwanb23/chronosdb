# Impact Engine Performance Report

- Result hash: `ed9b4e41240d955335bfdb4037e50541b76412d3efbc0a05bb7b960e1ab4ee0d`
- Platform: `Windows-11-10.0.26200-SP0`
- Python: `3.13.14`

- Db2: `not used by release-file benchmark`
- Dataset version: `1.0.0`
- Rule-set version: `impact-rules-v1.0.0`
- Scenario count per profile: `1` frozen golden scenario
- Error rate: `0.0` (failed executions are not included)
- Peak memory: `artifacts/phase-5/performance/memory.json`

Each profile measures one frozen golden request per sample. Profiles scale request load, not dataset cardinality; cold and cached state/totals are reported separately.

- `tiny` workload `1`: median `401.823 ms`, p95 `426.257 ms`, maximum `426.257 ms`, error rate `0.0`; artifact hash `ed6642c3336a7ca736547b0f25c7084db72741ad21f4b1b1147817ae58414395`
- `demo` workload `2`: median `412.697 ms`, p95 `438.806 ms`, maximum `438.806 ms`, error rate `0.0`; artifact hash `9a42bf1b7e7a03aaf733170b5b1d8786e3b7cd322dea117c2e703dad64aba584`
- `standard` workload `4`: median `420.327 ms`, p95 `440.203 ms`, maximum `440.203 ms`, error rate `0.0`; artifact hash `55eca234ae338e2c958200e67ba6557ccc30e457f3fd2322943c96fd86e5fd6e`
- `stress` workload `8`: median `413.383 ms`, p95 `471.098 ms`, maximum `471.098 ms`, error rate `0.0`; artifact hash `983726c73593bf625b05d36faf61f00a9d9d5ebee98a9aefbc0dbc54d425d82e`
