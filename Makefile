TEST=tests/
TEST_OPTS=

lint:
	black --check .

solution:
	pytest tests/solution.py

test:
	pytest $(TEST_OPTS) $(TEST)
