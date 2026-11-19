import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine

metadata = MetaData()


def open_engine() -> Engine:
    url = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    return create_engine(url, pool_pre_ping=True)
