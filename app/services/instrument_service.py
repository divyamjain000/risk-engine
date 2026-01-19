from typing import Any, List, Dict

import numpy as np
import pandas as pd

from app.brokers.groww_auth import get_access_token
from app.brokers.groww_adapter import GrowwAdapter

def _sanitize_dataframe(df: pd.DataFrame) -> List[Dict[str, Any]]:
    # Replace NaN/inf with None for JSON serialization
    clean = df.replace([np.inf, -np.inf], None).where(pd.notnull(df), None)
    return clean.to_dict(orient="records")


def fetch_instruments():
    token = get_access_token()
    groww = GrowwAdapter(token)

    data = groww.get_instruments()
    if isinstance(data, pd.DataFrame):
        return _sanitize_dataframe(data)
    return data
