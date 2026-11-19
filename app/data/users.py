from sqlalchemy import Column, Integer, String, Table, Uuid, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.engine import Engine

from app.data.database import metadata
from app.schemas import User

users = Table(
    "users",
    metadata,
    Column("sequence", Integer, primary_key=True),
    Column("id", Uuid, nullable=False, unique=True),
    Column("username", String(32), nullable=False),
    Column("username_key", String(32), nullable=False, unique=True),
    Column("display_name", String(100), nullable=False),
)


class UserStore:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def insert_if_absent(self, user: User) -> bool:
        insert = sqlite_insert if self.engine.dialect.name == "sqlite" else pg_insert
        statement = (
            insert(users)
            .values(**user.model_dump(), username_key=user.username.casefold())
            .on_conflict_do_nothing(index_elements=[users.c.username_key])
            .returning(users.c.id)
        )
        with self.engine.begin() as connection:
            return connection.scalar(statement) is not None

    def all(self) -> list[User]:
        statement = select(users.c.id, users.c.username, users.c.display_name).order_by(users.c.sequence)
        with self.engine.connect() as connection:
            return [User(**row) for row in connection.execute(statement).mappings()]
