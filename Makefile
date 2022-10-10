TEST=tests/
TEST_OPTS=

format:
	isort --profile=black .
	black .

lint:
	isort --check --profile=black .
	black --check .

solution:
	pytest tests/solution.py

test:
	pytest $(TEST_OPTS) $(TEST)
