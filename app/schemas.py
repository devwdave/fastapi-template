from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, HttpUrl, StringConstraints


class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Bookmark(BookmarkCreate):
    id: UUID
