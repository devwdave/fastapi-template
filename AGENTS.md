# Working on the FastAPI template

- Keep changes small enough to review in one sitting. Reuse existing code and give each new function a clear job.
- Register paths in `app/routes/`. Put HTTP inputs, responses, and error mapping in `app/handlers/`.
- Put business rules in `app/services/` and storage operations in `app/data/`. Keep request ID headers and logging in middleware.
- Manage dependencies with uv. Commit `uv.lock` when dependencies change.
- Run `make test` (or `uv run --locked pytest`) before finishing. When API behavior changes, cover it through a real endpoint in the test suite.
- Add an Alembic revision for schema changes. Exercise the migration against a fresh database before merging.
- When changing the container, build and run it using the commands in the README. Check that `GET /users` responds.
