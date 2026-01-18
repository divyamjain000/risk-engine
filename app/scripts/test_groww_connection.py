import json
from app.brokers.groww_auth import get_access_token_via_api_key
from app.brokers.groww_adapter import GrowwAdapter

def main():
    print("Generating Groww access token...")
    token = get_access_token_via_api_key()
    print("Token OK")

    groww = GrowwAdapter(token)

    print("\nFetching holdings...")
    holdings = groww.fetch_holdings()
    print(json.dumps(holdings, indent=2))

    print("\nFetching positions...")
    positions = groww.fetch_positions()
    print(json.dumps(positions, indent=2))

if __name__ == "__main__":
    main()
