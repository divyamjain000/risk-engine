import json
from app.brokers.groww_auth import get_access_token
from app.brokers.groww_adapter import GrowwAdapter

def main():
    print("Generating Groww access token...")
    token = get_access_token()
    print("Token OK")

    groww = GrowwAdapter(token)

    print("\nFetching holdings...")
    print(json.dumps(groww.get_holdings(), indent=2))

    print("\nFetching positions...")
    print(json.dumps(groww.get_positions(), indent=2))

    print("\nFetching margin details...")
    print(json.dumps(groww.get_available_margin_details(), indent=2))

if __name__ == "__main__":
    main()
