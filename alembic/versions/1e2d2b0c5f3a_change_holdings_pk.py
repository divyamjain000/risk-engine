"""change holdings_daily primary key to (symbol, as_of_date)

Revision ID: 1e2d2b0c5f3a
Revises: e04c908b310f
Create Date: 2026-01-19 16:40:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1e2d2b0c5f3a"
down_revision: Union[str, Sequence[str], None] = "e04c908b310f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing primary key on id and related indexes
    with op.batch_alter_table("holdings_daily") as batch:
        batch.drop_constraint("holdings_daily_pkey", type_="primary")
        # drop unique constraint if present
        batch.drop_constraint("uq_holdings_daily_symbol_date", type_="unique")
        # drop surrogate id column
        batch.drop_column("id")
        # add composite primary key
        batch.create_primary_key("pk_holdings_daily", ["symbol", "as_of_date"])
    # Recreate index on as_of_date if missing
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing_idx = {idx["name"] for idx in insp.get_indexes("holdings_daily")}
    if "ix_holdings_daily_as_of_date" not in existing_idx:
        op.create_index("ix_holdings_daily_as_of_date", "holdings_daily", ["as_of_date"], unique=False)


def downgrade() -> None:
    # Revert to surrogate id primary key with unique constraint
    with op.batch_alter_table("holdings_daily") as batch:
        batch.drop_constraint("pk_holdings_daily", type_="primary")
        batch.add_column(sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True))
        batch.create_primary_key("holdings_daily_pkey", ["id"])
        batch.create_unique_constraint("uq_holdings_daily_symbol_date", ["symbol", "as_of_date"])
    op.drop_index("ix_holdings_daily_as_of_date", table_name="holdings_daily")
