VENV := .venv
PY   := $(VENV)/bin/python

.PHONY: help setup build list test check-ascendants lint fmt clean deploy

help:
	@echo "setup   create .venv and install the project (editable, with dev extras)"
	@echo "build   build every mode into dist/"
	@echo "list    list the modes in this repo"
	@echo "deploy  build every mode and copy it into the game's scenario folder"
	@echo "test    run the test suite"
	@echo "check-ascendants  test, build, audit and map the Ascendants scenario"
	@echo "lint    run ruff"
	@echo "fmt     run ruff with --fix"
	@echo "clean   remove dist/ and Python caches"

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e ".[dev]"

build:
	$(PY) -m aoe2modes build --all

list:
	$(PY) -m aoe2modes list

deploy:
	$(PY) -m aoe2modes build --all --deploy

test:
	$(PY) -m pytest

# The audited filename is derived from mode.toml, so a version bump needs no edit here.
check-ascendants:
	$(PY) -m pytest tests/test_decompile.py tests/test_evolution_alpha.py
	$(PY) -m aoe2modes build evolution_alpha
	$(PY) -m aoe2modes audit "dist/$(shell $(PY) -m aoe2modes info evolution_alpha --output-name).aoe2scenario" --strict
	$(PY) -m aoe2modes map evolution_alpha --html dist/ascendants-map.html

lint:
	$(PY) -m ruff check .

fmt:
	$(PY) -m ruff check --fix .

clean:
	rm -rf dist
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache

# Normal and Speed candidates share gameplay code; validate both before publishing.
.PHONY: check-ra-speed
check-ra-speed:
	$(PY) -m pytest tests/test_evolution_alpha.py tests/test_ra_speed.py
	$(PY) -m ruff check modes/evolution_alpha modes/ra_speed tests/test_ra_speed.py tests/test_evolution_alpha.py
	$(PY) -m aoe2modes build evolution_alpha ra_speed
	$(PY) -m aoe2modes audit "dist/$(shell $(PY) -m aoe2modes info evolution_alpha --output-name).aoe2scenario" --strict
	$(PY) -m aoe2modes audit "dist/$(shell $(PY) -m aoe2modes info ra_speed --output-name).aoe2scenario" --strict
