"""update_instruments_table_schema

Revision ID: b3ae22bdebe6
Revises: 5c1b7e4c2d4a
Create Date: 2026-01-24 23:42:53.618887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3ae22bdebe6'
down_revision: Union[str, Sequence[str], None] = '5c1b7e4c2d4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    
    # Check if the table exists
    if not bind.dialect.has_table(bind, "instruments"):
        return
    
    # For both SQLite and PostgreSQL, we'll drop and recreate the table
    # This is safer for a schema change this significant
    
    # Drop existing table and index
    op.drop_index('ix_instruments_symbol', table_name='instruments')
    op.drop_table('instruments')
    
    # Create new table with updated schema
    op.create_table(
        'instruments',
        sa.Column('trading_symbol', sa.String(), primary_key=True, nullable=False),
        sa.Column('exchange', sa.String(), nullable=True),
        sa.Column('instrument_type', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('exchange_token', sa.String(), nullable=True),
        sa.Column('groww_symbol', sa.String(), nullable=True),
        sa.Column('segment', sa.String(), nullable=True),
        sa.Column('series', sa.String(), nullable=True),
        sa.Column('isin', sa.String(), nullable=True),
        sa.Column('underlying_symbol', sa.String(), nullable=True),
        sa.Column('underlying_exchange_token', sa.String(), nullable=True),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('strike_price', sa.Float(), nullable=True),
        sa.Column('lot_size', sa.Integer(), nullable=True),
        sa.Column('tick_size', sa.Float(), nullable=True),
        sa.Column('freeze_quantity', sa.Integer(), nullable=True),
        sa.Column('is_reserved', sa.Integer(), nullable=True),
        sa.Column('buy_allowed', sa.Integer(), nullable=True),
        sa.Column('sell_allowed', sa.Integer(), nullable=True),
    )
    op.create_index('ix_instruments_trading_symbol', 'instruments', ['trading_symbol'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    
    # Check if the table exists
    if not bind.dialect.has_table(bind, "instruments"):
        return
    
    # Drop the new table
    op.drop_index('ix_instruments_trading_symbol', table_name='instruments')
    op.drop_table('instruments')
    
    # Recreate old table with original schema
    op.create_table(
        'instruments',
        sa.Column('symbol', sa.String(), primary_key=True, nullable=False),
        sa.Column('exchange', sa.String(), nullable=True),
        sa.Column('instrument_type', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('exchange_token', sa.String(), nullable=True),
        sa.Column('groww_symbol', sa.String(), nullable=True),
    )
    op.create_index('ix_instruments_symbol', 'instruments', ['symbol'], unique=True)
