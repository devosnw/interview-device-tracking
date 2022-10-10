BLACK=black
ISORT=isort
PYTEST=pytest
TEST=tests/
TEST_OPTS=

.DEFAULT_GOAL := test

format:
	$(ISORT) --profile=black .
	$(BLACK) .

lint:
	$(ISORT) --check --profile=black .
	$(BLACK) --check .

solution:
	$(PYTEST) tests/solution.py

test:
	$(PYTEST) $(TEST_OPTS) $(TEST)
