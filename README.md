# FastAPI template

A small FastAPI starter with routes, handlers, a service layer, a data layer, and request ID middleware. The example creates user records with `POST /users` and lists them with `GET /users`. Each record has a UUID, a unique username, and a display name.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands from the repository root.

```sh
uv sync --locked
uv run pytest
uv run uvicorn app.main:app --reload
```

uv uses Python 3.12 by default, creates `.venv`, and installs the application and its development dependencies from `uv.lock`.

## Run with Docker

From the repository root, build the image and start the API.

```sh
docker build -t fastapi-template .
docker run --rm -p 127.0.0.1:8000:8000 fastapi-template
```

Leave the container running while you try the API. Press Ctrl+C to stop it. Each new container starts with an empty user collection.

## Run the API and PostgreSQL with Compose

Create a `.env` file in the repository root and set `POSTGRES_PASSWORD` to a local development password. Git ignores this file. Then start both services:

```sh
docker compose up --build --wait
```

The API listens on `127.0.0.1:8000`. Database clients on your machine can connect to `127.0.0.1:5432` using the database and user `app` and the password from `.env`. Inside the Compose network, the database address is `db:5432`. To open a SQL shell:

```sh
docker compose exec db psql -U app -d app
```

Run `docker compose down` to stop the stack. PostgreSQL keeps its data in the `pgdata` volume. The user endpoints still use the in-memory store.

If you reuse an existing database volume, set `POSTGRES_DB` and `POSTGRES_USER` in `.env` to its original database and role names. Compose uses the directory name as its default project name. After renaming a checkout, set `COMPOSE_PROJECT_NAME` to the previous project name to reconnect to its volume.

## Try the API

Open [the interactive API docs](http://127.0.0.1:8000/docs), expand **POST /users**, and choose **Try it out**. Submit this body:

```json
{"username": "ada", "display_name": "Ada Lovelace"}
```

The first request returns `201` and the saved user with its UUID. Submit it again to get `409`, then run **GET /users** to see the original entry. Each response includes an `X-Request-ID`. Find that value in the server log to see the method, path, and status for that request.

## Trace a request

1. [Routes](app/routes/users.py) register methods and paths with FastAPI.
2. [Handlers](app/handlers/users.py) receive validated input, call the service, and translate a duplicate into HTTP 409.
3. [The service](app/services/users.py) assigns a user ID and rejects duplicate usernames, ignoring case.
4. [The store](app/data/users.py) checks and inserts under one lock so concurrent requests cannot claim the same username.

[The app factory](app/main.py) connects the layers. [Request ID middleware](app/middleware/request_id.py) wraps the app and adds the same UUID to the response and log entry.

## Try this with Astra

> Replace the in-memory store with the PostgreSQL service in Compose. Preserve the existing API and tests, including duplicate handling. Add a test that saves a user, constructs a new app against the same database, and retrieves the user.
