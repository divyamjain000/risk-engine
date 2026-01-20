import json

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
from growwapi import GrowwAPI

SECRET_NAME = "groww/api"
REGION = "ap-south-1"

def _load_groww_secrets():
    try:
        client = boto3.client("secretsmanager", region_name=REGION)
        resp = client.get_secret_value(SecretId=SECRET_NAME)
        return json.loads(resp["SecretString"])
    except (NoCredentialsError, ClientError, ProfileNotFound) as exc:
        raise RuntimeError(f"Failed to retrieve Groww credentials from AWS Secrets Manager: {exc}") from exc

def get_access_token() -> str:
    secrets = _load_groww_secrets()

    api_key = secrets.get("GROWW_API_KEY")
    api_secret = secrets.get("GROWW_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("Missing GROWW_API_KEY or GROWW_API_SECRET")

    return GrowwAPI.get_access_token(
        api_key=api_key,
        secret=api_secret
    )
