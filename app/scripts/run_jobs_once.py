"""Manual runner for cron jobs to verify DB insertions.

Usage (from repo root):
  docker compose exec api python -m app.scripts.run_jobs_once

It will:
- Refresh instruments (truncate + insert latest)
- Upsert today's holdings snapshot
- Print counts and a few sample records
"""
import json
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import HoldingDaily, Instrument
from app.db.session import SessionLocal
from app.services.holdings_job import upsert_today_holdings
from app.services.instrument_job import replace_instruments, get_nse_bse_derivative_symbols


def _count_rows(session: Session, model) -> int:
    return session.query(func.count()).select_from(model).scalar() or 0


def _sample_rows(session: Session, model, limit: int = 5):
    return session.query(model).limit(limit).all()


def main():
    # Run instrument refresh
    inserted_instruments = replace_instruments()

    # Run holdings upsert for today
    inserted_holdings = upsert_today_holdings()

    # Summaries
    session: Session = SessionLocal()
    try:
        instruments_count = _count_rows(session, Instrument)
        holdings_count = _count_rows(session, HoldingDaily)
        sample_instruments = _sample_rows(session, Instrument)
        sample_holdings = (
            session.query(HoldingDaily)
            .filter(HoldingDaily.as_of_date == date.today())
            .limit(5)
            .all()
        )
        derivatives = get_nse_bse_derivative_symbols()[:10]
    finally:
        session.close()

    print("Instruments inserted:", inserted_instruments)
    print("Holdings upserted today:", inserted_holdings)
    print("Total instruments in DB:", instruments_count)
    print("Total holdings rows:", holdings_count)

    def _dump(objs):
        return json.dumps([obj.__dict__ for obj in objs], default=str, indent=2)

    print("\nSample instruments:")
    print(_dump(sample_instruments))

    print("\nSample holdings for today:")
    print(_dump(sample_holdings))

    print("\nSample NSE/BSE derivative symbols (max 10):")
    print(json.dumps(derivatives, indent=2))


if __name__ == "__main__":
    main()
