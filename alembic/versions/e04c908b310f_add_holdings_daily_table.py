"""add holdings daily table

Revision ID: e04c908b310f
Revises: 
Create Date: 2026-01-19 16:25:06.066329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e04c908b310f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if not insp.has_table("positions"):
        op.create_table(
            "positions",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("symbol", sa.String(), nullable=True),
            sa.Column("quantity", sa.Float(), nullable=True),
            sa.Column("avg_price", sa.Float(), nullable=True),
        )

    existing_pos_indexes = {idx["name"] for idx in insp.get_indexes("positions")}
    if "ix_positions_symbol" not in existing_pos_indexes:
        op.create_index("ix_positions_symbol", "positions", ["symbol"], unique=False)
    if "ix_positions_id" not in existing_pos_indexes:
        op.create_index("ix_positions_id", "positions", ["id"], unique=False)

    if not insp.has_table("holdings_daily"):
        op.create_table(
            "holdings_daily",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("symbol", sa.String(), nullable=False),
            sa.Column("as_of_date", sa.Date(), nullable=False),
            sa.Column("quantity", sa.Float(), nullable=False),
            sa.Column("avg_price", sa.Float(), nullable=True),
            sa.UniqueConstraint("symbol", "as_of_date", name="uq_holdings_daily_symbol_date"),
        )

    existing_hold_indexes = {idx["name"] for idx in insp.get_indexes("holdings_daily")} if insp.has_table("holdings_daily") else set()
    if "ix_holdings_daily_symbol" not in existing_hold_indexes:
        op.create_index("ix_holdings_daily_symbol", "holdings_daily", ["symbol"], unique=False)
    if "ix_holdings_daily_as_of_date" not in existing_hold_indexes:
        op.create_index("ix_holdings_daily_as_of_date", "holdings_daily", ["as_of_date"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_holdings_daily_as_of_date", table_name="holdings_daily")
    op.drop_index("ix_holdings_daily_symbol", table_name="holdings_daily")
    op.drop_table("holdings_daily")

    op.drop_index("ix_positions_id", table_name="positions")
    op.drop_index("ix_positions_symbol", table_name="positions")
    op.drop_table("positions")
