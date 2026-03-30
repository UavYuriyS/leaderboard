"""Add uid column to leaderboard users

Revision ID: 7a9e3b5c1d2f
Revises: 203ac1ae7571
Create Date: 2026-03-30 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a9e3b5c1d2f"
down_revision: Union[str, Sequence[str], None] = "203ac1ae7571"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("leaderboard", sa.Column("uid", sa.String(length=255), nullable=True))

    # Backfill existing rows with deterministic unique values.
    op.execute("UPDATE leaderboard SET uid = 'legacy-' || id::text WHERE uid IS NULL")

    op.alter_column("leaderboard", "uid", existing_type=sa.String(length=255), nullable=False)
    op.create_index(op.f("ix_leaderboard_uid"), "leaderboard", ["uid"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_leaderboard_uid"), table_name="leaderboard")
    op.drop_column("leaderboard", "uid")

