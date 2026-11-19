from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.data.database import open_engine
from app.data.users import UserStore
from app.middleware.request_id import RequestIDMiddleware
from app.routes.users import router
from app.services.users import UserService


@asynccontextmanager
async def lifespan(api: FastAPI):
    engine = open_engine()
    try:
        api.state.users = UserService(UserStore(engine))
        yield
    finally:
        engine.dispose()


def create_app() -> RequestIDMiddleware:
    api = FastAPI(title="FastAPI Template", lifespan=lifespan)
    api.include_router(router)
    # Wrap the whole app so even FastAPI's server-error responses get an ID.
    return RequestIDMiddleware(api)


app = create_app()
