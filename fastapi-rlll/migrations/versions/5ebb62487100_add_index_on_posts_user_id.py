"""add index on posts.user_id

Revision ID: 5ebb62487100
Revises: 05aca988b454
Create Date: 2026-09-19 12:10:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5ebb62487100"
down_revision: Union[str, Sequence[str], None] = "05aca988b454"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # PostgreSQL does not index foreign key columns automatically.
    op.create_index(op.f("ix_posts_user_id"), "posts", ["user_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_posts_user_id"), table_name="posts")
