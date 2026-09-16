"""add user_id to posts

Revision ID: 19443f0e599f
Revises: 23afb5d8c546
Create Date: 2026-09-11 20:08:48.208739

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "19443f0e599f"
down_revision: Union[str, Sequence[str], None] = "23afb5d8c546"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # posts created before auth existed have no owner - drop them so the
    # column below can be added as NOT NULL without a backfill.
    op.execute("DELETE FROM posts")
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_user_id_fkey", "posts", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_user_id_fkey", "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
