"""Create the example users table."""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("sequence", sa.Integer, primary_key=True),
        sa.Column("id", sa.Uuid, nullable=False, unique=True),
        sa.Column("username", sa.String(32), nullable=False),
        sa.Column("username_key", sa.String(32), nullable=False, unique=True),
        sa.Column("display_name", sa.String(100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
