# Working on the bookmarks API

- Keep changes small enough to review in one sitting. Reuse existing code and give each new function a clear job.
- Register paths in `app/routes/`. Put HTTP inputs, responses, and error mapping in `app/handlers/`.
- Put bookmark rules in `app/services/` and storage operations in `app/data/`. Keep request ID headers and logging in middleware.
- Manage dependencies with uv. Commit `uv.lock` when dependencies change.
- Run `uv run --locked pytest` before finishing. When API behavior changes, cover it through a real endpoint in the test suite.
- When changing the container, build and run it using the commands in the README. Check that `GET /bookmarks` responds.
