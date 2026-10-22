"""
Initial migration — create transcriptions table.

Revision: 0001_initial
"""

from typing import Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "transcriptions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("transcript", sa.Text, nullable=False),
        sa.Column("language", sa.String(20), nullable=True),
        sa.Column("duration_seconds", sa.Float, nullable=True),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_transcriptions_created_at", "transcriptions", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_transcriptions_created_at")
    op.drop_table("transcriptions")
