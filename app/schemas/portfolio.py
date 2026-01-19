from pydantic import BaseModel
from typing import List, Optional

class Holding(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    last_price: Optional[float] = None
    pnl: Optional[float] = None

class Position(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    side: str

class PortfolioResponse(BaseModel):
    holdings: List[Holding]
    positions: List[Position]
