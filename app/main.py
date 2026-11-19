from fastapi import FastAPI

from app.data.bookmarks import BookmarkStore
from app.middleware.request_id import RequestIDMiddleware
from app.routes.bookmarks import router
from app.services.bookmarks import BookmarkService


def create_app() -> RequestIDMiddleware:
    api = FastAPI(title="Bookmarks API")
    api.state.bookmarks = BookmarkService(BookmarkStore())
    api.include_router(router)
    # Wrap the whole app so even FastAPI's server-error responses get an ID.
    return RequestIDMiddleware(api)


app = create_app()
