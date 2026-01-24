from typing import Any

import pandas as pd
import numpy as np
import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.routers import groww as groww_router
from app.db import session as db_session_module


class MockInstrument:
    def __init__(self, trading_symbol, exchange, instrument_type, name, exchange_token, groww_symbol):
        self.trading_symbol = trading_symbol
        self.exchange = exchange
        self.instrument_type = instrument_type
        self.name = name
        self.exchange_token = exchange_token
        self.groww_symbol = groww_symbol


class MockQuery:
    def all(self):
        return [
            MockInstrument("FOO", "NSE", "EQ", None, "123", "NSE-FOO"),
            MockInstrument("BAR", "BSE", "EQ", "Bar Corp", "456", "BSE-BAR"),
        ]
    
    def filter(self, *args):
        # Simple mock - just return self for chaining
        return self
    
    def limit(self, n):
        # Simple mock - just return self for chaining
        return self


class MockSession:
    def query(self, model):
        return MockQuery()
    
    def close(self):
        pass


class StubClient:
    def __init__(self):
        self.last_args: dict[str, Any] = {}

    def get_holdings(self):
        return [{"trading_symbol": "TEST", "quantity": 1.0}]

    def get_positions_for_user(self, segment=None):
        self.last_args["segment"] = segment
        return [{"trading_symbol": "TEST-POS", "segment": segment or "EQUITY"}]

    def get_instruments(self):
        # Return a DataFrame including NaN/inf to validate sanitizer
        return pd.DataFrame(
            [
                {"exchange": "NSE", "exchange_token": "123", "trading_symbol": "FOO", "name": np.nan},
                {"exchange": "BSE", "exchange_token": "456", "trading_symbol": "BAR", "strike_price": np.inf},
            ]
        )


@pytest.fixture(autouse=True)
def disable_scheduler(monkeypatch):
    # Prevent scheduler jobs from starting during tests
    monkeypatch.setattr(main_module, "_start_scheduler", lambda: None, raising=False)
    monkeypatch.setattr(main_module, "_stop_scheduler", lambda: None, raising=False)


@pytest.fixture()
def client(monkeypatch):
    # Patch groww router client factory to use stub
    monkeypatch.setattr(groww_router, "_client", lambda: StubClient())
    
    from app.main import app
    from app.routers import instruments as instruments_router
    
    # Override database dependency to avoid real DB connection
    def override_get_db():
        yield MockSession()
    
    app.dependency_overrides[groww_router.get_db] = override_get_db
    # Also override instruments router to avoid DB connection
    app.dependency_overrides[instruments_router.get_db] = override_get_db
    
    yield TestClient(app)
    
    # Cleanup
    app.dependency_overrides.clear()


def test_holdings_ok(client: TestClient):
    resp = client.get("/groww/holdings")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data and data[0]["trading_symbol"] == "TEST"


def test_positions_segment_param(client: TestClient):
    resp = client.get("/groww/positions", params={"segment": "FNO"})
    assert resp.status_code == 200
    data = resp.json()
    assert data and data[0]["segment"] == "FNO"


def test_instruments_dataframe_sanitized(client: TestClient):
    resp = client.get("/groww/instruments")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    assert len(items) == 2
    # Should return instruments from mocked database
    first = items[0]
    assert first["trading_symbol"] == "FOO"
    assert first["exchange"] == "NSE"
    assert first.get("name") is None
    second = items[1]
    assert second["trading_symbol"] == "BAR"
    assert second["name"] == "Bar Corp"


def test_instruments_endpoint_exists(client: TestClient):
    """Test that the new instruments endpoint exists and returns data."""
    resp = client.get("/instruments/")
    # Should return 200 with list of instruments (might be empty if no data seeded)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
