from typing import List, Optional, Any
import logging

from fastapi import APIRouter, Body, Query, Depends, HTTPException
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.brokers.groww_adapter import GrowwAdapter
from app.brokers.groww_auth import get_access_token
from app.db.models import Instrument
from app.db.session import SessionLocal
from app.schemas.groww import PlaceOrderRequest, ModifyOrderRequest, OrderMarginRequest
from app.services.holdings_job import upsert_today_holdings
from app.services.instrument_job import replace_instruments

router = APIRouter(prefix="/groww", tags=["Groww"])
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _client() -> GrowwAdapter:
    token = get_access_token()
    return GrowwAdapter(token)


def _sanitize_dataframe(df: pd.DataFrame) -> list[dict[str, Any]]:
    clean = df.replace([np.inf, -np.inf], None).where(pd.notnull(df), None)
    return clean.to_dict(orient="records")

# Portfolio
@router.get("/portfolio")
def get_portfolio():
    return {
        "holdings": _client().get_holdings(),
        "positions": _client().get_positions_for_user(),
    }


@router.get("/holdings")
def get_holdings():
    return _client().get_holdings()


@router.get("/positions")
def get_positions(segment: Optional[str] = Query(None)):
    return _client().get_positions_for_user(segment=segment)


# Instruments and quotes
@router.get("/instruments")
def get_instruments(db: Session = Depends(get_db)):
    instruments = db.query(Instrument).all()
    return [
        {
            "symbol": inst.symbol,
            "exchange": inst.exchange,
            "instrument_type": inst.instrument_type,
            "name": inst.name,
            "exchange_token": inst.exchange_token,
            "groww_symbol": inst.groww_symbol,
        }
        for inst in instruments
    ]


@router.get("/quote")
def get_quote(trading_symbol: str, exchange: str, segment: str):
    return _client().get_quote(trading_symbol=trading_symbol, exchange=exchange, segment=segment)


@router.get("/ltp")
def get_ltp(segment: str, symbols: List[str] = Query(..., description="List of exchange:trading_symbol")):
    return _client().get_ltp(exchange_trading_symbols=tuple(symbols), segment=segment)


@router.get("/ohlc")
def get_ohlc(segment: str, symbols: List[str] = Query(..., description="List of exchange:trading_symbol")):
    return _client().get_ohlc(exchange_trading_symbols=tuple(symbols), segment=segment)


@router.get("/instrument/by-token/{exchange_token}")
def get_instrument_by_exchange_token(exchange_token: str):
    return _client().get_instrument_by_exchange_token(exchange_token=exchange_token)


@router.get("/instrument/by-symbol")
def get_instrument_by_exchange_and_trading_symbol(exchange: str, trading_symbol: str):
    return _client().get_instrument_by_exchange_and_trading_symbol(exchange=exchange, trading_symbol=trading_symbol)


@router.get("/instrument/by-groww/{groww_symbol}")
def get_instrument_by_groww_symbol(groww_symbol: str):
    return _client().get_instrument_by_groww_symbol(groww_symbol=groww_symbol)


# Derivatives and historical
@router.get("/expiries")
def get_expiries(exchange: str, underlying_symbol: str, year: Optional[int] = None, month: Optional[int] = None):
    return _client().get_expiries(exchange=exchange, underlying_symbol=underlying_symbol, year=year, month=month)


@router.get("/contracts")
def get_contracts(exchange: str, underlying_symbol: str, expiry_date: str):
    return _client().get_contracts(exchange=exchange, underlying_symbol=underlying_symbol, expiry_date=expiry_date)


@router.get("/greeks")
def get_greeks(exchange: str, underlying: str, trading_symbol: str, expiry: str):
    return _client().get_greeks(exchange=exchange, underlying=underlying, trading_symbol=trading_symbol, expiry=expiry)


@router.get("/historical/candle-data")
def get_historical_candle_data(
    trading_symbol: str,
    exchange: str,
    segment: str,
    start_time: str,
    end_time: str,
    interval_in_minutes: Optional[int] = None,
):
    return _client().get_historical_candle_data(
        trading_symbol=trading_symbol,
        exchange=exchange,
        segment=segment,
        start_time=start_time,
        end_time=end_time,
        interval_in_minutes=interval_in_minutes,
    )


@router.get("/historical/candles")
def get_historical_candles(
    exchange: str,
    segment: str,
    groww_symbol: str,
    start_time: str,
    end_time: str,
    candle_interval: str,
):
    return _client().get_historical_candles(
        exchange=exchange,
        segment=segment,
        groww_symbol=groww_symbol,
        start_time=start_time,
        end_time=end_time,
        candle_interval=candle_interval,
    )


# Orders and margins
@router.get("/orders")
def get_order_list(page: Optional[int] = 0, page_size: Optional[int] = 25, segment: Optional[str] = None):
    return _client().get_order_list(page=page, page_size=page_size, segment=segment)


@router.get("/orders/{order_id}")
def get_order_detail(order_id: str, segment: str):
    return _client().get_order_detail(segment=segment, groww_order_id=order_id)


@router.get("/orders/{order_id}/status")
def get_order_status(order_id: str, segment: str):
    return _client().get_order_status(segment=segment, groww_order_id=order_id)


@router.get("/orders/{order_id}/trades")
def get_trade_list_for_order(order_id: str, segment: str, page: Optional[int] = 0, page_size: Optional[int] = 25):
    return _client().get_trade_list_for_order(groww_order_id=order_id, segment=segment, page=page, page_size=page_size)


@router.post("/orders")
def place_order(payload: PlaceOrderRequest = Body(...)):
    return _client().place_order(
        validity=payload.validity,
        exchange=payload.exchange,
        order_type=payload.order_type,
        product=payload.product,
        quantity=payload.quantity,
        segment=payload.segment,
        trading_symbol=payload.trading_symbol,
        transaction_type=payload.transaction_type,
        order_reference_id=payload.order_reference_id,
        price=payload.price,
        trigger_price=payload.trigger_price,
    )


@router.post("/orders/{order_id}/modify")
def modify_order(order_id: str, payload: ModifyOrderRequest = Body(...)):
    return _client().modify_order(
        order_type=payload.order_type,
        segment=payload.segment,
        groww_order_id=order_id,
        quantity=payload.quantity,
        price=payload.price,
        trigger_price=payload.trigger_price,
    )


@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, segment: str):
    return _client().cancel_order(groww_order_id=order_id, segment=segment)


@router.get("/margin/available")
def get_available_margin_details():
    return _client().get_available_margin_details()


@router.post("/margin/orders")
def get_order_margin_details(payload: OrderMarginRequest = Body(...)):
    return _client().get_order_margin_details(segment=payload.segment, orders=payload.orders)


# Manual job triggers
@router.post("/jobs/{job_name}")
def trigger_job(job_name: str):
    """Manually trigger a cron job by name. Available jobs: holdings, instruments."""
    jobs = {
        "holdings": upsert_today_holdings,
        "instruments": replace_instruments,
    }
    
    if job_name not in jobs:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown job: {job_name}. Available: {', '.join(jobs.keys())}"
        )
    
    try:
        job_func = jobs[job_name]
        result = job_func()
        logger.info(f"Job {job_name} executed successfully, result: {result}")
        return {
            "job": job_name,
            "status": "success",
            "result": result
        }
    except Exception as e:
        logger.error(f"Job {job_name} failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Job {job_name} failed: {str(e)}"
        )
