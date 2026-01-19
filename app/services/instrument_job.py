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
        symbol = _extract_field(entry, ["symbol", "tradingSymbol", "trading_symbol", "tradingsymbol"])
        if not symbol:
            continue
        normalized.append(
            {
                "symbol": symbol,
                "exchange": _extract_field(entry, ["exchange"]),
                "instrument_type": _extract_field(entry, ["instrument_type", "instrumentType"]),
                "name": _extract_field(entry, ["name", "description", "instrument_name"]),
                "exchange_token": _extract_field(entry, ["exchange_token", "exchangeToken", "token", "exchangeTokenString"]),
                "groww_symbol": _extract_field(entry, ["groww_symbol", "growwInstrumentId", "groww_id"]),
            }
        )
    return normalized


def replace_instruments() -> int:
    items = fetch_instruments()
    if not items:
        return 0

    session: Session = SessionLocal()
    inserted = 0
    try:
        if not inspect(session.get_bind()).has_table(Instrument.__tablename__):
            return 0
        session.execute(delete(Instrument))
        for item in items:
            session.add(
                Instrument(
                    symbol=item.get("symbol"),
                    exchange=item.get("exchange"),
                    instrument_type=item.get("instrument_type"),
                    name=item.get("name"),
                    exchange_token=item.get("exchange_token"),
                    groww_symbol=item.get("groww_symbol"),
                )
            )
            inserted += 1
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    return inserted


def get_nse_bse_derivative_symbols() -> list[str]:
    """Return symbols listed on NSE/BSE that have futures or options contracts."""
    session: Session = SessionLocal()
    try:
        rows = (
            session.query(Instrument.symbol)
            .filter(Instrument.exchange.in_(["NSE", "BSE"]))
            .filter(Instrument.instrument_type.in_(DERIVATIVE_TYPES))
            .all()
        )
        return [r[0] for r in rows]
    finally:
        session.close()
