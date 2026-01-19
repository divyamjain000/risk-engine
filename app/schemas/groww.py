from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class PlaceOrderRequest(BaseModel):
    validity: str
    exchange: str
    order_type: str
    product: str
    quantity: int
    segment: str
    trading_symbol: str
    transaction_type: str
    order_reference_id: Optional[str] = None
    price: Optional[float] = 0.0
    trigger_price: Optional[float] = None

class ModifyOrderRequest(BaseModel):
    order_type: str
    segment: str
    quantity: int
    price: Optional[float] = None
    trigger_price: Optional[float] = None

class OrderMarginRequest(BaseModel):
    segment: str
    orders: List[Dict[str, Any]]
