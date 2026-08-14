PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python
CONFIG = config.txt

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

run:
	$(PYTHON_VENV) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON_VENV) -m pdb a_maze_ing.py $(CONFIG)

lint:
	$(PYTHON_VENV) -m flake8 --exclude=$(VENV) .
	$(PYTHON_VENV) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +