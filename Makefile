dev:
	uv run fastapi dev

r-check:
	uv run ruff check

r-fix:
	uv run ruff check --fix