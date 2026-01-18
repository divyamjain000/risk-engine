import json
import boto3
from growwapi import GrowwAPI

SECRET_NAME = "groww/api"
REGION = "ap-south-1"

def _load_groww_secrets():
    client = boto3.client("secretsmanager", region_name=REGION)
    resp = client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(resp["SecretString"])

def get_access_token_via_api_key() -> str:
    secrets = _load_groww_secrets()

    api_key = secrets.get("GROWW_API_KEY")
    api_secret = secrets.get("GROWW_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("Groww credentials missing in Secrets Manager")

    return GrowwAPI.get_access_token(
        api_key=api_key,
        secret=api_secret
    )
