from fastapi import APIRouter, status

from app.handlers.users import create_user, list_users

router = APIRouter(tags=["users"])
router.add_api_route("/users", list_users, methods=["GET"])
router.add_api_route(
    "/users",
    create_user,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Username already taken"}},
)
