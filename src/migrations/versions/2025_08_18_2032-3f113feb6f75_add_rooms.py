"""add rooms

Revision ID: 3f113feb6f75
Revises: 11b555c680b3
Create Date: 2025-08-18 20:32:31.327268

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3f113feb6f75"
down_revision: Union[str, Sequence[str], None] = "11b555c680b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
