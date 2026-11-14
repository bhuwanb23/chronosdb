25. Repository Structure
docker/
├── db2/
├── backend/
└── frontend/

scripts/
├── setup.sh
├── db_up.sh
├── migrate.sh
├── seed.py
├── build_embeddings.py
├── run_demo.sh
└── health_check.py

sql/
├── migrations/
└── seeds/

artifacts/
└── reproducibility/

docs/reproducibility/
├── reproducibility-architecture.md
├── version-matrix.md
├── health-checks.md
├── troubleshooting.md
├── install-test-report.md
└── phase-15-completion-report.md

Makefile
docker-compose.yml
.env.example

