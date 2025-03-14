dev:
	uv run fastapi dev

r-check:
	uv run ruff check

r-fix:
	uv run ruff check --fix

r-format:
	uv run ruff format