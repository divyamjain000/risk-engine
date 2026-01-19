from datetime import datetime, timedelta
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.services.holdings_job import upsert_today_holdings
from app.services.instrument_job import replace_instruments

_scheduler: AsyncIOScheduler | None = None
logger = logging.getLogger(__name__)

def start_scheduler() -> None:
    """Configure and start the shared AsyncIO scheduler."""
    global _scheduler
    if _scheduler and _scheduler.running:
        logger.info("Scheduler already running; skipping start.")
        return

    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(upsert_today_holdings, CronTrigger(hour=2, minute=0), id="holdings-daily", replace_existing=True)
    scheduler.add_job(replace_instruments, CronTrigger(hour=3, minute=0), id="instruments-daily", replace_existing=True)

    # Run once shortly after startup to ensure fresh data without waiting for the first window
    now = datetime.utcnow()
    scheduler.add_job(upsert_today_holdings, trigger="date", run_date=now + timedelta(seconds=5), id="holdings-seed", replace_existing=True)
    scheduler.add_job(replace_instruments, trigger="date", run_date=now + timedelta(seconds=10), id="instruments-seed", replace_existing=True)

    scheduler.start()
    _scheduler = scheduler
    logger.info("Scheduler started with daily and seed jobs")

def stop_scheduler() -> None:
    """Stop the shared scheduler if running."""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("Scheduler stopped")
