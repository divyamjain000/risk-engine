from datetime import date
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.brokers.groww_adapter import GrowwAdapter
from app.brokers.groww_auth import get_access_token
from app.db.models import HoldingDaily
from app.db.session import SessionLocal


def _normalize_symbol(entry: Dict[str, Any]) -> Optional[str]:
    return (
        entry.get("symbol")
        or entry.get("trading_symbol")
        or entry.get("tradingSymbol")
        or entry.get("tradingsymbol")
    )


def _normalize_holding(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    symbol = _normalize_symbol(entry)
    if not symbol:
        return None
    quantity = entry.get("quantity") or entry.get("qty") or entry.get("net_qty")
    avg_price = entry.get("avg_price") or entry.get("average_price") or entry.get("avgPrice")
    return {"symbol": symbol, "quantity": quantity or 0.0, "avg_price": avg_price}


def fetch_holdings() -> List[Dict[str, Any]]:
    token = get_access_token()
    client = GrowwAdapter(token)
    data = client.get_holdings()
    if isinstance(data, dict) and "holdings" in data:
        data = data.get("holdings", [])
    if not isinstance(data, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        parsed = _normalize_holding(entry)
        if parsed:
            normalized.append(parsed)
    return normalized


def upsert_today_holdings() -> int:
    today = date.today()
    holdings = fetch_holdings()
    if not holdings:
        return 0

    session: Session = SessionLocal()
    inserted_or_updated = 0
    try:
        for h in holdings:
            symbol = h["symbol"]
            quantity = h.get("quantity", 0.0) or 0.0
            avg_price = h.get("avg_price")
            existing = session.get(HoldingDaily, {"symbol": symbol, "as_of_date": today})
            if existing:
                existing.quantity = quantity
                existing.avg_price = avg_price
            else:
                session.add(
                    HoldingDaily(
                        symbol=symbol,
                        as_of_date=today,
                        quantity=quantity,
                        avg_price=avg_price,
                    )
                )
            inserted_or_updated += 1
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    return inserted_or_updated
