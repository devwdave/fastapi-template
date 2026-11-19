from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.schemas import Bookmark, BookmarkCreate
from app.services.bookmarks import BookmarkService, DuplicateBookmark


def get_service(request: Request) -> BookmarkService:
    return request.app.state.bookmarks


Service = Annotated[BookmarkService, Depends(get_service)]


def create_bookmark(data: BookmarkCreate, service: Service) -> Bookmark:
    try:
        return service.create(data)
    except DuplicateBookmark as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc


def list_bookmarks(service: Service) -> list[Bookmark]:
    return service.list_bookmarks()
