from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from sqlalchemy import delete, inspect
from sqlalchemy.orm import Session

from app.brokers.groww_adapter import GrowwAdapter
from app.brokers.groww_auth import get_access_token
from app.db.models import Instrument
from app.db.session import SessionLocal

DERIVATIVE_TYPES = {
    "FUT",
    "OPT",
    "FUTIDX",
    "FUTSTK",
    "OPTIDX",
    "OPTSTK",
}


def _sanitize_dataframe(df: pd.DataFrame) -> List[Dict[str, Any]]:
    clean = df.replace([np.inf, -np.inf], None).where(pd.notnull(df), None)
    return clean.to_dict(orient="records")


def _extract_field(entry: Dict[str, Any], keys: List[str]) -> Optional[Any]:
    for k in keys:
        if k in entry and entry[k] is not None:
            return entry[k]
    return None


def fetch_instruments() -> List[Dict[str, Any]]:
    token = get_access_token()
    client = GrowwAdapter(token)
    data = client.get_instruments()
    if isinstance(data, pd.DataFrame):
        data = _sanitize_dataframe(data)
    if not isinstance(data, list):
        return []

    normalized: List[Dict[str, Any]] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        trading_symbol = _extract_field(entry, ["trading_symbol", "tradingSymbol", "symbol", "tradingsymbol"])
        if not trading_symbol:
            continue
        normalized.append(
            {
                "trading_symbol": trading_symbol,
                "exchange": _extract_field(entry, ["exchange"]),
                "instrument_type": _extract_field(entry, ["instrument_type", "instrumentType"]),
                "name": _extract_field(entry, ["name", "description", "instrument_name"]),
                "exchange_token": _extract_field(entry, ["exchange_token", "exchangeToken", "token", "exchangeTokenString"]),
                "groww_symbol": _extract_field(entry, ["groww_symbol", "growwInstrumentId", "groww_id"]),
                "segment": _extract_field(entry, ["segment"]),
                "series": _extract_field(entry, ["series"]),
                "isin": _extract_field(entry, ["isin"]),
                "underlying_symbol": _extract_field(entry, ["underlying_symbol", "underlyingSymbol"]),
                "underlying_exchange_token": _extract_field(entry, ["underlying_exchange_token", "underlyingExchangeToken"]),
                "expiry_date": _extract_field(entry, ["expiry_date", "expiryDate", "expiry"]),
                "strike_price": _extract_field(entry, ["strike_price", "strikePrice", "strike"]),
                "lot_size": _extract_field(entry, ["lot_size", "lotSize"]),
                "tick_size": _extract_field(entry, ["tick_size", "tickSize"]),
                "freeze_quantity": _extract_field(entry, ["freeze_quantity", "freezeQuantity"]),
                "is_reserved": _extract_field(entry, ["is_reserved", "isReserved"]),
                "buy_allowed": _extract_field(entry, ["buy_allowed", "buyAllowed"]),
                "sell_allowed": _extract_field(entry, ["sell_allowed", "sellAllowed"]),
            }
        )
    return normalized


def replace_instruments() -> int:
    items = fetch_instruments()
    if not items:
        return 0

    session: Session = SessionLocal()
    try:
        if not inspect(session.get_bind()).has_table(Instrument.__tablename__):
            return 0
        
        # Delete all existing records first and commit
        session.execute(delete(Instrument))
        session.commit()
        
        # Deduplicate items by trading_symbol (keep last occurrence)
        seen = {}
        for item in items:
            trading_symbol = item.get("trading_symbol")
            if trading_symbol:
                seen[trading_symbol] = item
        
        # Bulk insert deduplicated instruments
        instruments = [
            Instrument(
                trading_symbol=item.get("trading_symbol"),
                exchange=item.get("exchange"),
                instrument_type=item.get("instrument_type"),
                name=item.get("name"),
                exchange_token=item.get("exchange_token"),
                groww_symbol=item.get("groww_symbol"),
                segment=item.get("segment"),
                series=item.get("series"),
                isin=item.get("isin"),
                underlying_symbol=item.get("underlying_symbol"),
                underlying_exchange_token=item.get("underlying_exchange_token"),
                expiry_date=item.get("expiry_date"),
                strike_price=item.get("strike_price"),
                lot_size=item.get("lot_size"),
                tick_size=item.get("tick_size"),
                freeze_quantity=item.get("freeze_quantity"),
                is_reserved=item.get("is_reserved"),
                buy_allowed=item.get("buy_allowed"),
                sell_allowed=item.get("sell_allowed"),
            )
            for item in seen.values()
        ]
        session.bulk_save_objects(instruments)
        session.commit()
        return len(instruments)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_nse_bse_derivative_symbols() -> list[str]:
    """Return symbols listed on NSE/BSE that have futures or options contracts."""
    session: Session = SessionLocal()
    try:
        rows = (
            session.query(Instrument.trading_symbol)
            .filter(Instrument.exchange.in_(["NSE", "BSE"]))
            .filter(Instrument.instrument_type.in_(DERIVATIVE_TYPES))
            .all()
        )
        return [r[0] for r in rows]
    finally:
        session.close()
