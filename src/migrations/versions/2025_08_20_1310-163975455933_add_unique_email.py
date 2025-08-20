"""add unique email

Revision ID: 163975455933
Revises: e8458f9e916a
Create Date: 2025-08-20 13:10:43.683167

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "163975455933"
down_revision: Union[str, Sequence[str], None] = "e8458f9e916a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
