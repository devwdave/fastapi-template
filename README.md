# FastAPI bookmarks template

Save a bookmark with `POST /bookmarks` and read the collection with `GET /bookmarks`. The app keeps bookmarks in insertion order in memory. Each worker has its own collection, and restarting the server clears it.

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
docker build -t bookmarks-api .
docker run --rm -p 127.0.0.1:8000:8000 bookmarks-api
```

Leave the container running while you try the API. Press Ctrl+C to stop it. Each new container starts with an empty bookmark collection.

## Run the API and PostgreSQL with Compose

Create a `.env` file in the repository root and set `POSTGRES_PASSWORD` to a local development password. Git ignores this file. Then start both services:

```sh
docker compose up --build --wait
```

The API listens on `127.0.0.1:8000`. Database clients on your machine can connect to `127.0.0.1:5432` using the database and user `bookmarks` and the password from `.env`. Inside the Compose network, the database address is `db:5432`. To open a SQL shell:

```sh
docker compose exec db psql -U bookmarks -d bookmarks
```

Run `docker compose down` to stop the stack. PostgreSQL keeps its data in the `pgdata` volume. The bookmark endpoints still use the in-memory store.

## Try the API

Open [the interactive API docs](http://127.0.0.1:8000/docs), expand **POST /bookmarks**, and choose **Try it out**. Submit this body:

```json
{"url": "https://example.org/", "title": "Example"}
```

The first request returns `201` and the saved bookmark with its UUID. Submit it again to get `409`, then run **GET /bookmarks** to see the original entry. Each response includes an `X-Request-ID`. Find that value in the server log to see the method, path, and status for that request.

## Trace a request

1. [Routes](app/routes/bookmarks.py) register methods and paths with FastAPI.
2. [Handlers](app/handlers/bookmarks.py) receive validated input, call the service, and translate a duplicate into HTTP 409.
3. [The service](app/services/bookmarks.py) assigns a bookmark ID and enforces uniqueness by normalized URL.
4. [The store](app/data/bookmarks.py) checks and inserts under one lock so concurrent saves cannot create duplicates.

[The app factory](app/main.py) connects the layers. [Request ID middleware](app/middleware/request_id.py) wraps the app and adds the same UUID to the response and log entry.

## Try this with Astra

> Replace the in-memory store with SQLite. Preserve the existing API and tests, including duplicate handling. Add a test that saves a bookmark, constructs a new app against the same database, and retrieves the bookmark.
