"""add_index_on_underlying_symbol

Revision ID: 796e56818781
Revises: b3ae22bdebe6
Create Date: 2026-01-25 00:03:23.224079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '796e56818781'
down_revision: Union[str, Sequence[str], None] = 'b3ae22bdebe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    
    # Check if the table exists
    if not bind.dialect.has_table(bind, "instruments"):
        return
    
    # Create index on underlying_symbol
    op.create_index('ix_instruments_underlying_symbol', 'instruments', ['underlying_symbol'])


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    
    # Check if the table exists
    if not bind.dialect.has_table(bind, "instruments"):
        return
    
    # Drop the index
    op.drop_index('ix_instruments_underlying_symbol', table_name='instruments')
