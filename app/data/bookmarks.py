from threading import Lock

from app.schemas import Bookmark


class BookmarkStore:
    def __init__(self) -> None:
        self._by_url: dict[str, Bookmark] = {}
        self._lock = Lock()

    def insert_if_absent(self, bookmark: Bookmark) -> bool:
        key = str(bookmark.url)
        with self._lock:
            if key in self._by_url:
                return False
            self._by_url[key] = bookmark
            return True

    def all(self) -> list[Bookmark]:
        with self._lock:
            return list(self._by_url.values())
