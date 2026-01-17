from fastapi import APIRouter

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("")
def get_portfolio():
    return {
        "total_capital": 342000,
        "cash": 92000,
        "max_drawdown_pct": 12,
        "current_drawdown_pct": 4.1,
        "risk_per_trade": 1500
    }
