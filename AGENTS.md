# Working on the FastAPI template

## Where code belongs

Keep route registration and HTTP handling in separate modules. The `POST /users` endpoint illustrates the boundary.

- **Routes** (`app/routes/`) map paths and HTTP methods to handler functions and declare response metadata such as the `201` success status.
- **Handlers** (`app/handlers/`) receive validated input, call the service, and translate outcomes into HTTP responses. In `create_user`, the handoff is `service.create(data)`. The handler translates `DuplicateUser` into HTTP `409`.
- **Services** (`app/services/`) own business decisions. `UserService.create` assigns a UUID and raises `DuplicateUser` when the store reports a conflict. Keep services callable from a CLI or job without a FastAPI request or an HTTP exception.
- **Data** (`app/data/`) owns queries, transactions, and atomic writes. The user store reports whether an insert succeeded. The database enforces uniqueness even when requests arrive together.
- Put input and output shapes in `app/schemas.py`, shared HTTP behavior such as request ID logging in `app/middleware/`, and dependency wiring in `app/main.py`.

## Design principles

- **KISS (Keep It Simple).** Choose the clearest implementation that satisfies the requirement. Give each function one job and keep changes small enough to review in one sitting.
- **YAGNI (You Aren’t Gonna Need It).** Add a base class, plugin hook, or configuration option when a current caller needs it. A possible future resource is insufficient reason to add a generic service.
- **DRY (Don’t Repeat Yourself).** Give each business rule one owner so every caller gets the same behavior. Extract shared code when its callers should change together. Similar-looking code can serve different rules.

## Python conventions

- Use `snake_case` for functions and variables and `PascalCase` for classes. Choose names that explain intent, such as `insert_if_absent`.
- Type function parameters and return values at layer boundaries. Prefer built-in annotations such as `list[User]` and `User | None`.
- For an optional list or dict argument, default to `None` and create the collection inside the function. This gives each call its own collection.
- Use context managers for connections and transactions. Catch the specific exceptions a layer can handle, and preserve the cause with `raise ... from exc` when translating an error.
- Match the existing synchronous store with synchronous handlers. Use `async def` for asynchronous I/O and keep blocking database calls off the event loop.

## Dependencies and verification

- Manage dependencies with uv. Commit `uv.lock` when dependencies change.
- Run `make test` (or `uv run --locked pytest`) before finishing. When API behavior changes, cover it through a real endpoint in the test suite.
- Add an Alembic revision for schema changes. Exercise the migration against a fresh database before merging.
- When changing the container, build and run it using the commands in the README. Check that `GET /users` responds.
