PYTHON=poetry
FMT=black
DEVELOPER=0
ARGS=""

default: fmt check

dep:
	$(PYTHON) install

fmt:
	$(PYTHON) run $(FMT) .

check:
	$(PYTHON) run pytest tests

env:
	$(PYTHON) shell

clean:
	rm -rf .venv **/__p*