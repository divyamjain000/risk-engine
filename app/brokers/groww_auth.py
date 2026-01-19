import json
import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from growwapi import GrowwAPI

SECRET_NAME = "groww/api"
REGION = "ap-south-1"

def _load_groww_secrets():
    env_key = os.getenv("GROWW_API_KEY")
    env_secret = os.getenv("GROWW_API_SECRET")
    if env_key and env_secret:
        return {"GROWW_API_KEY": env_key, "GROWW_API_SECRET": env_secret}

    try:
        client = boto3.client("secretsmanager", region_name=REGION)
        resp = client.get_secret_value(SecretId=SECRET_NAME)
        return json.loads(resp["SecretString"])
    except (NoCredentialsError, ClientError) as exc:
        raise RuntimeError("AWS credentials not configured; provide GROWW_API_KEY and GROWW_API_SECRET env vars for local runs") from exc

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
