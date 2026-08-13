PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON_VENV) main.py

debug:
	$(PYTHON_VENV) -m pdb main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	$(VENV)/bin/flake8 . && $(VENV)/bin/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs