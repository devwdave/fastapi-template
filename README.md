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
