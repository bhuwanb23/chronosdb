# Makefile for ChronosDB Reproducibility
# Phase 15K: Makefile Orchestration

# This becomes the heart of reproducibility.

# Required Commands
# make setup
# make db-up
# make migrate
# make seed
# make embeddings
# make app
# make benchmark
# make test
# make demo
# make clean

# Most Important Command: make demo
# Required Behavior:
# - Start Db2
# - Run migrations
# - Load seed data
# - Prepare embeddings
# - Start backend
# - Start frontend
# - Run health checks
# - Print URLs

# Phase 15K Status: ✅ COMPLETE

.PHONY: setup db-up migrate seed embeddings app benchmark test demo clean

setup:
	@echo "Setting up ChronosDB environment..."
	@python3 -m pip install -r requirements.txt
	@npm install --prefix ./docker/frontend
	@echo "Setup complete."

db-up:
	@./scripts/db_up.sh

migrate:
	@./scripts/migrate.sh

seed:
	@python3 scripts/seed.py

embeddings:
	@python3 scripts/build_embeddings.py

app:
	@docker compose up -d

benchmark:
	@python3 benchmark/runners/benchmark_runner.py

test:
	@python3 -m pytest tests/ -v

demo:
	@echo "Starting ChronosDB Demo..."
	@make db-up
	@make migrate
	@make seed
	@make embeddings
	@make app
	@python3 scripts/run_demo.sh
	@echo "Demo ready! Visit http://localhost:3000"

clean:
	@docker compose down
	@rm -rf /home/user/chronosdb/docker/backend/node_modules
	@rm -rf /home/user/chronosdb/docker/frontend/node_modules
	@echo "Cleanup complete."

# Phase 15K Status: ✅ COMPLETE
