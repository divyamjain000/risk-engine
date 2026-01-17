from fastapi import FastAPI
from app.routers import portfolio

app = FastAPI(title="Risk Engine API")
app.include_router(portfolio.router)

@app.get("/")
def root():
    return {"status": "ok"}
