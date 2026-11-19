from threading import Lock

from app.schemas import User


class UserStore:
    def __init__(self) -> None:
        self._by_username: dict[str, User] = {}
        self._lock = Lock()

    def insert_if_absent(self, user: User) -> bool:
        key = user.username.casefold()
        with self._lock:
            if key in self._by_username:
                return False
            self._by_username[key] = user
            return True

    def all(self) -> list[User]:
        with self._lock:
            return list(self._by_username.values())
