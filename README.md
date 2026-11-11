# ChronosDB

ChronosDB is an auditable counterfactual decision system for supply-chain
disruptions. Phase 0 establishes the application and Db2 foundation; domain
tables, simulation, optimization, retrieval, and the UI are intentionally
deferred to later phases.

## Phase 0 foundation

- Python 3.11–3.13 and FastAPI
- IBM Db2 through `ibm_db`
- Environment-based configuration with no committed secrets
- Separate liveness and Db2 readiness endpoints
- Idempotent health-table bootstrap and health-check script

## Local setup

1. Install Python 3.11 or newer (less than 3.14).
2. Make a virtual environment and install the project:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -e ".[dev]"
   ```

3. Copy `.env.example` to `.env` and set the local Db2 values. The password
   must be a real local credential in `.env`; it must never be committed.
4. Create the configured schema in Db2, then bootstrap the foundation table:

   ```powershell
   python scripts\db_health.py --bootstrap
   ```

5. Start the API:

   ```powershell
   python -m uvicorn chronosdb.main:app --reload
   ```

The API is available at `http://127.0.0.1:8000`.

## Health endpoints

- `GET /health/live` works without Db2 and confirms that the process is alive.
- `GET /health/ready` checks configuration and executes a read-only Db2 query.
- `GET /version` returns application and schema versions without credentials.

## Development commands

```powershell
python -m ruff check .
python -m mypy src
python -m pytest
```

Db2 integration tests are opt-in:

```powershell
$env:RUN_DB2_INTEGRATION_TESTS = "1"
python -m pytest -m db2
```

## Project boundaries

This repository is being developed as the ChronosDB product itself. The
competition and submission workflow described in the original planning notes is
not part of the implementation. The next engineering phase defines the
supply-chain entities and deterministic business rules.
