from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Instrument
from app.db.session import SessionLocal
from app.schemas.instruments import Instrument as InstrumentSchema

router = APIRouter(prefix="/instruments", tags=["Instruments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/underlying/{underlying_symbol}", response_model=List[InstrumentSchema])
def get_instruments_by_underlying(
    underlying_symbol: str,
    instrument_type: Optional[str] = None,
    segment: Optional[str] = None,
    exchange: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Fetch instruments by underlying symbol (options/futures contracts).
    
    Args:
        underlying_symbol: The underlying instrument symbol (e.g., 'BANKNIFTY', 'NIFTY', 'RELIANCE')
        instrument_type: Optional filter by instrument type (e.g., 'CE', 'PE', 'FUT')
        segment: Optional filter by segment (e.g., 'FNO')
        exchange: Optional filter by exchange (e.g., 'NSE', 'BSE')
        limit: Maximum number of results (default: 100, max: 1000)
        
    Returns:
        List of all options/futures contracts for the given underlying symbol
    """
    query = db.query(Instrument).filter(Instrument.underlying_symbol == underlying_symbol)
    
    if instrument_type:
        query = query.filter(Instrument.instrument_type == instrument_type)
    
    if segment:
        query = query.filter(Instrument.segment == segment)
    
    if exchange:
        query = query.filter(Instrument.exchange == exchange)
    
    # Limit results
    limit = min(limit, 1000)
    instruments = query.limit(limit).all()
    
    return instruments


@router.get("/{trading_symbol}", response_model=InstrumentSchema)
def get_instrument_by_symbol(trading_symbol: str, db: Session = Depends(get_db)):
    """
    Fetch a single instrument by its trading symbol.
    
    Args:
        trading_symbol: The instrument trading symbol (e.g., 'RELIANCE', 'BANKNIFTY25DEC27000PE')
        
    Returns:
        Instrument details including exchange, type, name, options data, etc.
    """
    instrument = db.query(Instrument).filter(Instrument.trading_symbol == trading_symbol).first()
    
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Instrument with trading symbol '{trading_symbol}' not found")
    
    return instrument


@router.get("/", response_model=List[InstrumentSchema])
def get_instruments(
    exchange: Optional[str] = None,
    instrument_type: Optional[str] = None,
    segment: Optional[str] = None,
    underlying_symbol: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Fetch instruments with optional filters.
    
    Args:
        exchange: Filter by exchange (e.g., 'NSE', 'BSE')
        instrument_type: Filter by instrument type (e.g., 'EQ', 'CE', 'PE', 'FUT')
        segment: Filter by segment (e.g., 'EQ', 'FNO')
        underlying_symbol: Filter by underlying symbol (e.g., 'BANKNIFTY', 'NIFTY')
        limit: Maximum number of results (default: 100, max: 1000)
        
    Returns:
        List of instruments matching the filters
    """
    query = db.query(Instrument)
    
    if exchange:
        query = query.filter(Instrument.exchange == exchange)
    
    if instrument_type:
        query = query.filter(Instrument.instrument_type == instrument_type)
    
    if segment:
        query = query.filter(Instrument.segment == segment)
    
    if underlying_symbol:
        query = query.filter(Instrument.underlying_symbol == underlying_symbol)
    
    # Limit results
    limit = min(limit, 1000)
    instruments = query.limit(limit).all()
    
    return instruments
