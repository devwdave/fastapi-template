from alembic import context

from app.data.database import metadata, open_engine
from app.data import users  # Register the example table for autogeneration.

engine = open_engine()
try:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()
finally:
    engine.dispose()
