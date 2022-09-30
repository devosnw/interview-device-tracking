TEST=tests/
TEST_OPTS=

solution:
	pytest tests/solution.py

test:
	pytest $(TEST_OPTS) $(TEST)
