"""rename users.hash_password to password_hash

Revision ID: 05aca988b454
Revises: 19443f0e599f
Create Date: 2026-09-19 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "05aca988b454"
down_revision: Union[str, Sequence[str], None] = "19443f0e599f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # A plain rename keeps every stored hash. Autogenerate would emit
    # drop_column + add_column here and wipe all passwords.
    op.alter_column("users", "hash_password", new_column_name="password_hash")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users", "password_hash", new_column_name="hash_password")
