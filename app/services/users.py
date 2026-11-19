from uuid import uuid4

from app.data.users import UserStore
from app.schemas import User, UserCreate


class DuplicateUser(Exception):
    pass


class UserService:
    def __init__(self, store: UserStore) -> None:
        self.store = store

    def create(self, data: UserCreate) -> User:
        user = User(id=uuid4(), username=data.username, display_name=data.display_name)
        if not self.store.insert_if_absent(user):
            raise DuplicateUser("This username is already taken.")
        return user

    def list_users(self) -> list[User]:
        return self.store.all()
