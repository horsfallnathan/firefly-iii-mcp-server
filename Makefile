# Makefile for firefly-mcp project
.PHONY: help test-unit test-integration test-all app dev coverage clean docs docs-serve docs-build docs-deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  test-unit        - Run unit tests only (uses .env.test)"
	@echo "  test-integration - Run integration tests only (uses .env.test)"  
	@echo "  test-all         - Run all tests (uses .env.test)"
	@echo "  dev              - Run development server with .env"
	@echo "  dev-test         - Run development server with .env.test"
	@echo "  coverage         - Generate coverage report"
	@echo "  docs-serve       - Serve documentation locally"
	@echo "  docs-build       - Build documentation"
	@echo "  docs-deploy      - Deploy documentation to GitHub Pages"
	@echo "  clean            - Clean up generated files"
	@echo ""
	@echo "Pass pytest flags with ARGS variable:"
	@echo "  make test-unit ARGS='--maxfail=1'"
	@echo "  make test-all ARGS='-v -s'"

# Test commands
test-unit:
	uv run --env-file .env.test pytest tests -m 'not integration' --ignore=tests/integration $(ARGS)

test-integration:
	uv run --env-file .env.test pytest tests/integration -m integration -v $(ARGS)

test-all:
	uv run --env-file .env.test pytest tests $(ARGS)

app:
	uv run --env-file .env python -m firefly_mcp.main

# Development server commands
dev:
	uv run --env-file .env.dev python -m firefly_mcp.main

# Utility commands
coverage:
	uv run --env-file .env.test pytest tests --cov=src/firefly_mcp --cov-report=html $(ARGS)

# Documentation commands
docs-serve:
	uv run --group docs mkdocs serve

docs-build:
	uv run --group docs mkdocs build

docs-deploy:
	uv run --group docs mkdocs gh-deploy

# Clean up
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
