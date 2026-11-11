6. Phase 0E: Engineering Environment Baseline
Goal

Make developer behavior reproducible before building domain logic.

Recommended baseline
Backend
Python 3.11 or 3.12
FastAPI
Pydantic v2
ibm_db
SQLAlchemy plus ibm_db_sa, only if tested against the selected Db2 version
LangChain
pytest
Ruff
MyPy
Bandit
pip-audit
Frontend
Node.js 20 LTS or newer supported LTS
TypeScript
React
Vite or Next.js
ESLint
Vitest
General
Git
Make
Docker-compatible runtime if supported
Visual Studio Code
Java 17 for the Db2 Developer Extension

The official extension documentation currently lists Visual Studio Code 1.103.0 or newer and Java 17 or newer as prerequisites.

### Subphase 0E.1: Version manifest

### Create:

docs/project-control/version-matrix.md


### Include:

| Component | Required | Detected | Verification command |
| --- | --- | --- | --- |
| Python | 3.11.x or chosen version | Actual | python --version |
| Node.js | Chosen LTS | Actual | node --version |
| npm | Locked | Actual | npm --version |
| Java | 17+ | Actual | java -version |
| Git | Recorded | Actual | git --version |
| Db2 | Exact edition/version | Actual | Db2 version query |
| ibm_db | Locked | Actual | Package query |
Subphase 0E.2: Dependency locking

### Do not rely solely on broad ranges such as:

fastapi>=0.100


Create deterministic locks or exact package versions.

### Subphase 0E.3: Standard commands

### The following command contract should exist:

make doctor
make install
make lint
make typecheck
make test
make validate-submission
make security
make db-health


## Phase 0 does not need make demo; that comes later.

## Environment benchmark

### On a clean checkout:

Environment diagnosis: under 30 seconds
Dependency installation: ideally under 10 minutes on normal broadband
Lint and foundation tests: under 2 minutes
No undocumented global Python or Node dependency
Same test result on two consecutive runs
