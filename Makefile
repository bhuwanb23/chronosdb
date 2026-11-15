# ChronosDB reproducibility Makefile (Phase 15K)
# Fresh clone -> make setup -> make demo

PYTHON ?= $(shell command -v python3 2>/dev/null || command -v python)
NPM ?= npm
COMPOSE ?= docker compose

.PHONY: setup db-up db-check migrate seed validate-seed embeddings embedding-check \
	backend frontend app benchmark test health demo clean validate-phase15 \
	impact-intake-check impact-golden-input-check impact-benchmark-manifest-check \
	impact-golden impact-benchmark impact-performance impact-handoff impact-validate

setup:
	@bash scripts/setup.sh

db-up:
	@bash scripts/db_up.sh

db-check:
	@bash scripts/db_check.sh

migrate:
	@bash scripts/migrate.sh

seed:
	@$(PYTHON) scripts/seed.py

validate-seed:
	@$(PYTHON) scripts/seed.py --validate-only

embeddings:
	@$(PYTHON) scripts/build_embeddings.py

embedding-check:
	@$(PYTHON) scripts/build_embeddings.py --check

backend:
	@PYTHONPATH=src:. $(PYTHON) -m uvicorn backend.chronosdb.api.app:app --host 0.0.0.0 --port 8000

frontend:
	@cd src/frontend && $(NPM) run dev -- --host 0.0.0.0 --port 3000

app:
	@$(COMPOSE) up -d --build

benchmark:
	@$(PYTHON) benchmark/runners/benchmark_runner.py

test:
	@$(PYTHON) -m pytest tests -q

health:
	@$(PYTHON) scripts/health_check.py --retries 30

demo: db-up migrate seed embeddings app health
	@bash scripts/run_demo.sh

clean:
	@$(COMPOSE) down -v --remove-orphans || true
	@rm -rf .pytest_cache .coverage htmlcov
	@rm -rf src/frontend/node_modules
	@echo "Cleanup complete."

validate-phase15:
	@$(PYTHON) scripts/validate_phase15.py

impact-intake-check:
	@$(PYTHON) scripts/impact_intake.py --check all

impact-golden-input-check:
	@$(PYTHON) scripts/impact_intake.py --check golden

impact-benchmark-manifest-check:
	@$(PYTHON) scripts/impact_intake.py --check benchmark

impact-golden:
	@$(PYTHON) scripts/run_phase5_golden.py

impact-benchmark:
	@$(PYTHON) scripts/run_impact_benchmarks.py

impact-performance:
	@$(PYTHON) scripts/run_impact_performance.py

impact-handoff:
	@$(PYTHON) scripts/build_phase5_handoff.py

impact-validate:
	@$(PYTHON) scripts/validate_phase5.py
