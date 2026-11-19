.DEFAULT_GOAL := help
.PHONY: help setup dev test migrate up down logs

help:
	@echo "make setup    Install the locked Python dependencies"
	@echo "make dev      Apply migrations and run the API with reload"
	@echo "make test     Run endpoint tests against isolated databases"
	@echo "make migrate  Apply pending migrations to the configured database"
	@echo "make up       Build and start the API and PostgreSQL with Compose"
	@echo "make down     Stop the Compose stack and keep its data"
	@echo "make logs     Follow Compose logs"

setup:
	uv sync --locked

migrate:
	uv run --locked python -m alembic upgrade head

dev: migrate
	uv run --locked python -m uvicorn app.main:app --reload

test:
	uv run --locked pytest

up:
	docker compose up --build --wait

down:
	docker compose down

logs:
	docker compose logs -f
