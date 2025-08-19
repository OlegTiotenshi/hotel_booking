"""add users

Revision ID: e8458f9e916a
Revises: 3f113feb6f75
Create Date: 2025-08-19 17:22:47.544614

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e8458f9e916a"
down_revision: Union[str, Sequence[str], None] = "3f113feb6f75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
