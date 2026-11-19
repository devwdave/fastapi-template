from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StringConstraints


class UserCreate(BaseModel):
    username: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=32, pattern=r"^[A-Za-z0-9_]+$")
    ]
    display_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class User(UserCreate):
    id: UUID
