"""seed_sample_instruments

Revision ID: c30a497fb3ff
Revises: 796e56818781
Create Date: 2026-01-25 00:11:44.293930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c30a497fb3ff'
down_revision: Union[str, Sequence[str], None] = '796e56818781'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - seed sample instruments."""
    bind = op.get_bind()
    
    # Check if the table exists
    if not bind.dialect.has_table(bind, "instruments"):
        return
    
    # Simple insert without parameters
    inserts = [
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, exchange_token, groww_symbol, segment, series, isin) VALUES ('RELIANCE', 'NSE', 'EQ', 'Reliance Industries Ltd', '2885', 'NSE-RELIANCE', 'EQ', 'EQ', 'INE002A01018')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, exchange_token, groww_symbol, segment, series, isin) VALUES ('TCS', 'NSE', 'EQ', 'Tata Consultancy Services', '2456', 'NSE-TCS', 'EQ', 'EQ', 'INE467B01029')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, exchange_token, groww_symbol, segment, series, isin) VALUES ('INFY', 'BSE', 'EQ', 'Infosys Ltd', '500209', 'BSE-INFY', 'EQ', 'EQ', 'INE009A01021')",
        
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('BANKNIFTY25JAN24000CE', 'NSE', 'CE', 'BANKNIFTY 24 JAN 24000 CE', 'FNO', 'CE', 'BANKNIFTY', 15, 5.0, 24000.0, '2026-01-24')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('BANKNIFTY25JAN24000PE', 'NSE', 'PE', 'BANKNIFTY 24 JAN 24000 PE', 'FNO', 'PE', 'BANKNIFTY', 15, 5.0, 24000.0, '2026-01-24')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('BANKNIFTY25JAN24500CE', 'NSE', 'CE', 'BANKNIFTY 24 JAN 24500 CE', 'FNO', 'CE', 'BANKNIFTY', 15, 5.0, 24500.0, '2026-01-24')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('BANKNIFTY25JAN24500PE', 'NSE', 'PE', 'BANKNIFTY 24 JAN 24500 PE', 'FNO', 'PE', 'BANKNIFTY', 15, 5.0, 24500.0, '2026-01-24')",
        
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('NIFTY25JAN23000CE', 'NSE', 'CE', 'NIFTY 24 JAN 23000 CE', 'FNO', 'CE', 'NIFTY', 50, 5.0, 23000.0, '2026-01-24')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('NIFTY25JAN23000PE', 'NSE', 'PE', 'NIFTY 24 JAN 23000 PE', 'FNO', 'PE', 'NIFTY', 50, 5.0, 23000.0, '2026-01-24')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('NIFTY25JAN23500CE', 'NSE', 'CE', 'NIFTY 24 JAN 23500 CE', 'FNO', 'CE', 'NIFTY', 50, 5.0, 23500.0, '2026-01-24')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, strike_price, expiry_date) VALUES ('NIFTY25JAN23500PE', 'NSE', 'PE', 'NIFTY 24 JAN 23500 PE', 'FNO', 'PE', 'NIFTY', 50, 5.0, 23500.0, '2026-01-24')",
        
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, expiry_date) VALUES ('BANKNIFTYFUT25JAN', 'NSE', 'FUT', 'BANKNIFTY JAN 2026 FUTURE', 'FNO', 'FUT', 'BANKNIFTY', 15, 5.0, '2026-01-29')",
        "INSERT INTO instruments (trading_symbol, exchange, instrument_type, name, segment, series, underlying_symbol, lot_size, tick_size, expiry_date) VALUES ('NIFTYFUT25JAN', 'NSE', 'FUT', 'NIFTY JAN 2026 FUTURE', 'FNO', 'FUT', 'NIFTY', 50, 5.0, '2026-01-29')",
    ]
    
    for sql in inserts:
        op.execute(sa.text(sql))


def downgrade() -> None:
    """Downgrade schema - remove seeded instruments."""
    bind = op.get_bind()
    
    # Check if the table exists
    if not bind.dialect.has_table(bind, "instruments"):
        return
    
    # Delete seeded records
    op.execute(sa.text(
        "DELETE FROM instruments WHERE trading_symbol IN ('BANKNIFTY25JAN24000CE', 'BANKNIFTY25JAN24000PE', 'BANKNIFTY25JAN24500CE', 'BANKNIFTY25JAN24500PE', 'NIFTY25JAN23000CE', 'NIFTY25JAN23000PE', 'NIFTY25JAN23500CE', 'NIFTY25JAN23500PE', 'BANKNIFTYFUT25JAN', 'NIFTYFUT25JAN', 'RELIANCE', 'TCS', 'INFY')"
    ))
