PYTHON = python3

install:
	$(PYTHON) -m pip install -i requirements.txt

run:
	$(PYTHON) main.py

debug:
	$(PYTHON) -m pdb main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .

lint-strict:
	flake8 --select=E, F .
