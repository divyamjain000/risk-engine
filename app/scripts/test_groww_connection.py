import json
from app.brokers.groww_auth import get_access_token
from app.brokers.groww_adapter import GrowwAdapter

def main():
    print("Generating Groww access token...")
    token = get_access_token()
    print("Token OK")

    groww = GrowwAdapter(token)

    print("\nFetching holdings...")
    print(json.dumps(groww.fetch_holdings(), indent=2))

    print("\nFetching positions...")
    print(json.dumps(groww.fetch_positions(), indent=2))

if __name__ == "__main__":
    main()
