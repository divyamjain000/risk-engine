from pydantic import BaseModel
from typing import Optional

class Instrument(BaseModel):
    symbol: str
    exchange: str
    instrument_type: str
    name: Optional[str] = None
