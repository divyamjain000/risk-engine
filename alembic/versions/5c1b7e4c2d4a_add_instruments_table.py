"""add instruments table

Revision ID: 5c1b7e4c2d4a
Revises: 1e2d2b0c5f3a
Create Date: 2026-01-19 17:05:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5c1b7e4c2d4a"
down_revision: Union[str, Sequence[str], None] = "1e2d2b0c5f3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not op.get_bind().dialect.has_table(op.get_bind(), "instruments"):
        op.create_table(
            "instruments",
            sa.Column("symbol", sa.String(), primary_key=True, nullable=False),
            sa.Column("exchange", sa.String(), nullable=True),
            sa.Column("instrument_type", sa.String(), nullable=True),
            sa.Column("name", sa.String(), nullable=True),
            sa.Column("exchange_token", sa.String(), nullable=True),
            sa.Column("groww_symbol", sa.String(), nullable=True),
        )
        op.create_index("ix_instruments_symbol", "instruments", ["symbol"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_instruments_symbol", table_name="instruments")
    op.drop_table("instruments")
