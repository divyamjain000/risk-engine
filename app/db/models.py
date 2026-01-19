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

    symbol = Column(String, primary_key=True, index=True, nullable=False)
    exchange = Column(String, nullable=True)
    instrument_type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    exchange_token = Column(String, nullable=True)
    groww_symbol = Column(String, nullable=True)
