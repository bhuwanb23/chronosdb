# 19J: Reproducibility Review
| Step | Result |
|---|---|
| `make setup` | **FAIL**: `docker/frontend` missing |
| `make demo` | **Not run**: no Docker/Db2 in sandbox |
| `pip install -r requirements.txt` | not re-run here; `fastapi` was missing and had to be installed by hand |
| Test suite | 73 failed, 118 passed, 4 collection errors |
| Fresh-environment review by independent reviewer | **Not done** |
Verdict: **FAIL**. A new user cannot complete setup without assistance.
