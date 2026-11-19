from fastapi import APIRouter, status

from app.handlers.bookmarks import create_bookmark, list_bookmarks

router = APIRouter(tags=["bookmarks"])
router.add_api_route("/bookmarks", list_bookmarks, methods=["GET"])
router.add_api_route(
    "/bookmarks",
    create_bookmark,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "URL already bookmarked"}},
)
