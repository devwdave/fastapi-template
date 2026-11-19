# FastAPI template

Start a backend with one working resource. `POST /users` creates a user and `GET /users` lists saved records. Both endpoints return an `X-Request-ID` you can look up in the server logs.

## First run

Choose **Use this template** on GitHub, clone your new repository, and open a terminal at its root. Install [uv](https://docs.astral.sh/uv/getting-started/installation/). With GNU Make installed:

```sh
make dev
```

This installs the locked dependencies, applies the first migration to a local SQLite file (`app.db`), and starts the reload server. Open [the API docs](http://127.0.0.1:8000/docs) and try **POST /users** with:

```json
{"username": "ada", "display_name": "Ada Lovelace"}
```

Run **GET /users** to see the saved UUID and names. Records survive a server restart. Stop the server with Ctrl+C.

## Run with PostgreSQL

Set `POSTGRES_PASSWORD` to a development password in a `.env` file at the repo root. Git ignores the file. With Docker Compose installed, run:

```sh
make up
```

Compose starts PostgreSQL 18, waits for the database, applies Alembic migrations, and starts the API on port 8000. Stop the local dev server first if it already uses that port. Open a SQL shell to inspect the rows:

```sh
docker compose exec db psql -U app -d app -c "SELECT id, username, display_name FROM users"
```

The host database address is `127.0.0.1:5432`. The default database and role are both `app`. `make down` stops both services and keeps the named database volume. If reusing an existing volume, set `POSTGRES_DB`, `POSTGRES_USER`, and `COMPOSE_PROJECT_NAME` to the values used when you created it.

For an external PostgreSQL instance, set `DATABASE_URL` in your shell to a SQLAlchemy URL starting with `postgresql+psycopg://`. Both the API and Alembic read it. The local SQLite file and Compose's PostgreSQL volume are separate databases.

## Make this template yours in five minutes

1. **Name the backend.** Set the package name and description in `pyproject.toml`, run `uv lock`, and change the FastAPI title in [app/main.py](app/main.py). That title appears at `/docs`.
2. **Define your first resource.** For a projects API, start with `ProjectCreate` and `Project` in [app/schemas.py](app/schemas.py). Use [routes/users.py](app/routes/users.py) as the example for registering `POST /projects` and `GET /projects`. The [handler](app/handlers/users.py) translates HTTP errors, and the [service](app/services/users.py) holds business rules.
3. **Give it storage.** Define the table and its queries in `app/data/projects.py` using the shared metadata in [database.py](app/data/database.py). Import the new table module in [migrations/env.py](migrations/env.py). From a migrated dev database, run `uv run --locked python -m alembic revision --autogenerate -m "create projects"`, review the generated revision, then run `make migrate`.
4. **Wire it up and test it.** In [app/main.py](app/main.py), construct the store and service and include the router. Adapt [the endpoint tests](tests/test_users.py) to your resource, run `make test`, and try the endpoint at `/docs`.
5. **Retire the example when ready.** Remove the users router, service wiring, and unused modules. Update the Docker smoke test to call your new endpoint. For a database already in use, keep applied migration files and retire the users table in a new revision after its data has been accounted for.

## Command reference

Run `make` to see the shortcuts. The underlying commands also work directly in PowerShell or a Unix shell.

| Task | Make | Underlying command |
| --- | --- | --- |
| Install dependencies | `make setup` | `uv sync --locked` |
| Apply migrations | `make migrate` | `uv run --locked python -m alembic upgrade head` |
| Start with reload | `make dev` | Apply migrations, then `uv run --locked python -m uvicorn app.main:app --reload` |
| Run isolated tests | `make test` | `uv run --locked pytest` |
| Start the PostgreSQL stack | `make up` | `docker compose up --build --wait` |
| Follow container logs | `make logs` | `docker compose logs -f` |
| Stop the stack | `make down` | `docker compose down` |

To run the image on its own with SQLite, use a volume for the database file:

```sh
docker build -t fastapi-template .
docker run --rm -p 127.0.0.1:8000:8000 -v fastapi-data:/data fastapi-template
```
