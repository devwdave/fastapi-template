from uuid import uuid4

from app.data.bookmarks import BookmarkStore
from app.schemas import Bookmark, BookmarkCreate


class DuplicateBookmark(Exception):
    pass


class BookmarkService:
    def __init__(self, store: BookmarkStore) -> None:
        self.store = store

    def create(self, data: BookmarkCreate) -> Bookmark:
        bookmark = Bookmark(id=uuid4(), title=data.title, url=data.url)
        if not self.store.insert_if_absent(bookmark):
            raise DuplicateBookmark("This URL is already bookmarked.")
        return bookmark

    def list_bookmarks(self) -> list[Bookmark]:
        return self.store.all()
