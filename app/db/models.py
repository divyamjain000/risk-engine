from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Float)
    avg_price = Column(Float)


class HoldingDaily(Base):
    __tablename__ = "holdings_daily"

    symbol = Column(String, primary_key=True, index=True, nullable=False)
    as_of_date = Column(Date, primary_key=True, index=True, nullable=False)
    quantity = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=True)


class Instrument(Base):
    __tablename__ = "instruments"

    trading_symbol = Column(String, primary_key=True, index=True, nullable=False)
    exchange = Column(String, index=True, nullable=True)
    exchange_token = Column(String, nullable=True)
    groww_symbol = Column(String, nullable=True)
    name = Column(String, nullable=True)
    instrument_type = Column(String, index=True, nullable=True)
    segment = Column(String, nullable=True)
    series = Column(String, nullable=True)
    isin = Column(String, nullable=True)
    underlying_symbol = Column(String, nullable=True)
    underlying_exchange_token = Column(String, nullable=True)
    expiry_date = Column(Date, nullable=True)
    strike_price = Column(Float, nullable=True)
    lot_size = Column(Integer, nullable=True)
    tick_size = Column(Float, nullable=True)
    freeze_quantity = Column(Integer, nullable=True)
    is_reserved = Column(Integer, nullable=True)
    buy_allowed = Column(Integer, nullable=True)
    sell_allowed = Column(Integer, nullable=True)
