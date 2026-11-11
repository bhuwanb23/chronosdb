.PHONY: install run lint typecheck test test-db2 db-bootstrap db-health doctor

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

run:
	python -m uvicorn chronosdb.main:app --reload

lint:
	python -m ruff check .

typecheck:
	python -m mypy src

test:
	python -m pytest

test-db2:
	set RUN_DB2_INTEGRATION_TESTS=1 && python -m pytest -m db2

db-bootstrap:
	python scripts/db_health.py --bootstrap

db-health:
	python scripts/db_health.py

doctor:
	python --version
	python -m pip --version
	python -c "import fastapi, ibm_db, pydantic_settings; print('Python dependencies: OK')"
