5. Phase 0D: Repository and Submission Workspace
Goal

Create a repository structure that passes the official validator and remains maintainable.

## Canonical setup

### Use the canonical repository described in the submission guide:

git clone https://github.com/<username>/IBM_Db2_TechX_Project_Submission.git
cd IBM_Db2_TechX_Project_Submission
git remote add upstream https://github.com/KunalGolaIBM/IBM_Db2_TechX_Project_Submission.git
git fetch upstream main
git checkout -b submission/chronosdb upstream/main
cp -r submissions/_template submissions/chronosdb


The official guide specifies this fork, branch and template workflow.

Target structure
submissions/chronosdb/
├── README.md
├── architecture.md
├── submission.json
├── .env.example
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── package.json
├── src/
│   ├── backend/
│   │   └── chronosdb/
│   │       ├── api/
│   │       ├── core/
│   │       ├── db/
│   │       ├── domain/
│   │       ├── services/
│   │       └── main.py
│   └── frontend/
├── sql/
│   ├── migrations/
│   ├── seeds/
│   └── health/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/
├── benchmarks/
├── scripts/
├── docs/
│   ├── screenshots/
│   ├── project-control/
│   └── evidence/
└── artifacts/

Required initial files
submission.json

Populate all known fields with valid, honest values. Do not leave invalid placeholders that break JSON.

.env.example

### Only variable names and dummy values:

DB2_HOST=localhost
DB2_PORT=50000
DB2_DATABASE=CHRONOS
DB2_USERNAME=db2inst1
DB2_PASSWORD=replace-me
DB2_SCHEMA=CHRONOS
LLM_PROVIDER=disabled
LLM_API_KEY=replace-me
LOG_LEVEL=INFO
APP_ENV=development


Never commit .env.

.gitignore

### Include:

.env
.env.*
!.env.example
__pycache__/
*.pyc
.venv/
node_modules/
dist/
coverage/
.pytest_cache/
*.log
.DS_Store

## Local submission validation

### The repository provides:

python scripts/validate_submission.py submissions/chronosdb


Run this in Phase 0 and in CI. The submission guide explicitly recommends the local validator.

Benchmarks
| Test | Target |
| --- | --- |
| Official validator | 100% pass |
| Required files present | 4/4 |
| Invalid JSON | 0 |
| Files outside project folder changed | 0 |
| Broken internal documentation links | 0 |
| Untracked required source files | 0 |
Exit criterion

A clean branch containing only the foundation structure passes the official validator.

