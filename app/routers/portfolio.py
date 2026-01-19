from fastapi import APIRouter
from app.services.portfolio_service import fetch_portfolio

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("/")
def get_portfolio():
    return fetch_portfolio()
