.PHONY: install test benchmark benchmark-real-world clean

PYTHON ?= python3.11
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

install:
	test -d "$(VENV)" || $(PYTHON) -m venv "$(VENV)"
	$(PY) -m ensurepip --upgrade
	$(PIP) install --upgrade pip
	$(PIP) install -e "./code[dev,h3]"

test:
	cd code && ../$(PY) -m pytest tests -v

benchmark:
	cd code && ../$(PY) scripts/run_benchmark.py

benchmark-real-world:
	cd code && ../$(PY) scripts/prepare_real_world_fixtures.py

clean:
	rm -rf code/dist code/build
