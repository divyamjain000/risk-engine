from fastapi import FastAPI
from app.db.base import init_db
from app.routers import portfolio

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(portfolio.router)

@app.get("/")
def health():
    return {"status": "ok"}
