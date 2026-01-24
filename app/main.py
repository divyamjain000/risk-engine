from fastapi import FastAPI

from app.routers import groww as groww_router
from app.routers import instruments as instruments_router
from app.scheduler import start_scheduler as _start_scheduler, stop_scheduler as _stop_scheduler

app = FastAPI(title="Risk Engine API")

app.include_router(groww_router.router)
app.include_router(instruments_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def start_scheduler():
    _start_scheduler()


@app.on_event("shutdown")
def stop_scheduler():
    _stop_scheduler()
