from fastapi import FastAPI

from app.data.users import UserStore
from app.middleware.request_id import RequestIDMiddleware
from app.routes.users import router
from app.services.users import UserService


def create_app() -> RequestIDMiddleware:
    api = FastAPI(title="FastAPI Template")
    api.state.users = UserService(UserStore())
    api.include_router(router)
    # Wrap the whole app so even FastAPI's server-error responses get an ID.
    return RequestIDMiddleware(api)


app = create_app()
