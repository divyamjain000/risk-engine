import json
import boto3
from datetime import date
from typing import Dict

BUCKET = "risk-engine-datalake-340632003931"

s3 = boto3.client("s3")

def write_portfolio_snapshot(portfolio_id: int, snapshot: Dict):
    key = f"snapshots/portfolio_id={portfolio_id}/date={date.today().isoformat()}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(snapshot),
        ContentType="application/json"
    )

    return key
