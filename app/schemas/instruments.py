from pydantic import BaseModel
from typing import Optional
from datetime import date

class Instrument(BaseModel):
    trading_symbol: str
    exchange: Optional[str] = None
    exchange_token: Optional[str] = None
    groww_symbol: Optional[str] = None
    name: Optional[str] = None
    instrument_type: Optional[str] = None
    segment: Optional[str] = None
    series: Optional[str] = None
    isin: Optional[str] = None
    underlying_symbol: Optional[str] = None
    underlying_exchange_token: Optional[str] = None
    expiry_date: Optional[date] = None
    strike_price: Optional[float] = None
    lot_size: Optional[int] = None
    tick_size: Optional[float] = None
    freeze_quantity: Optional[int] = None
    is_reserved: Optional[int] = None
    buy_allowed: Optional[int] = None
    sell_allowed: Optional[int] = None
    
    class Config:
        from_attributes = True
