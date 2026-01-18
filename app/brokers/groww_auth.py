import os
from growwapi import GrowwAPI

def get_access_token_via_api_key() -> str:
    """
    Generates Groww access token using API key + API secret.
    Required env vars:
      - GROWW_API_KEY
      - GROWW_API_SECRET
    """
    api_key = os.getenv("GROWW_API_KEY")
    api_secret = os.getenv("GROWW_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("Missing GROWW_API_KEY or GROWW_API_SECRET")

    access_token = GrowwAPI.get_access_token(
        api_key=api_key,
        secret=api_secret
    )

    return access_token
