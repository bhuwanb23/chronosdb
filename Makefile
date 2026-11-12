.PHONY: install run lint typecheck test test-db2 db-bootstrap db-health doctor \
	data-clean data-generate data-validate ground-truth data-report data-checksums data-all

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

data-clean:
	python scripts/data_pipeline.py --clean

data-generate:
	python scripts/data_pipeline.py

data-validate:
	python scripts/validate_release.py

ground-truth:
	python scripts/build_golden.py
	python scripts/build_benchmarks.py --scale standard

data-report:
	python scripts/report_dataset.py

data-checksums:
	python scripts/generate_checksums.py

data-all:
	python scripts/data_pipeline.py --clean
