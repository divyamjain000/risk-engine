from app.brokers.groww_auth import get_access_token
from app.brokers.groww_adapter import GrowwAdapter

def fetch_portfolio():
    token = get_access_token()
    groww = GrowwAdapter(token)

    holdings = groww.get_holdings()
    positions = groww.get_positions()

    return {
        "holdings": holdings,
        "positions": positions,
    }
