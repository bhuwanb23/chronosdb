# Impact Engine Performance Report

- Result hash: `a75b7947e0ea958ad7d8139dd19ef77f243d620cf07741738a9f51e9040713ea`
- Platform: `Windows-11-10.0.26200-SP0`
- Python: `3.13.14`

- Db2: `not used by release-file benchmark`
- Dataset version: `1.0.0`
- Rule-set version: `impact-rules-v1.0.0`
- Scenario count per profile: `1` frozen golden scenario
- Error rate: `0.0` (failed executions are not included)
- Peak memory: `artifacts/phase-5/performance/memory.json`
- Targets: demo state `<500 ms` and total `<2 s`; standard state `<1.5 s` and total `<6 s`.

Each profile measures one frozen golden request per sample. Profiles scale request load, not dataset cardinality; cold and cached state/totals are reported separately.

- `tiny` workload `1`: samples `4`, median `455.699 ms`, p95 `495.445 ms`, maximum `495.445 ms`, error rate `0.0`; artifact hash `58cc21a82412e6db0cee0150b153942500ebe82eff2494744c344e979b2fcfd6`
- `demo` workload `2`: samples `3`, median `428.251 ms`, p95 `500.927 ms`, maximum `500.927 ms`, error rate `0.0`; artifact hash `f4bd4ce4ea82613b1a30883e6f820fd889ced85ee89ce04a03647bb93319b5b4`
- `standard` workload `4`: samples `3`, median `409.782 ms`, p95 `424.138 ms`, maximum `424.138 ms`, error rate `0.0`; artifact hash `7a651581999a34f0454fd7515138f0d65b4f7576e4d1d17aee218db9e2dda883`
- `stress` workload `8`: samples `3`, median `490.526 ms`, p95 `492.405 ms`, maximum `492.405 ms`, error rate `0.0`; artifact hash `df51f4f2cdd0ff96ac48e24df0cde178243add0e09b21684b57a1986ddea0dfe`
