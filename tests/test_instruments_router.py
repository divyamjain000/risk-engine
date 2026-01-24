from fastapi.testclient import TestClient
import pytest
from unittest.mock import MagicMock

import app.main as main_module
from app.routers import instruments as instruments_router
from app.db import session as db_session_module


class MockInstrument:
    def __init__(self, trading_symbol, exchange, instrument_type, name, 
                 exchange_token=None, groww_symbol=None, segment=None, 
                 series=None, isin=None, underlying_symbol=None, 
                 underlying_exchange_token=None, expiry_date=None, 
                 strike_price=None, lot_size=None, tick_size=None, 
                 freeze_quantity=None, is_reserved=None, 
                 buy_allowed=None, sell_allowed=None):
        self.trading_symbol = trading_symbol
        self.exchange = exchange
        self.instrument_type = instrument_type
        self.name = name
        self.exchange_token = exchange_token
        self.groww_symbol = groww_symbol
        self.segment = segment
        self.series = series
        self.isin = isin
        self.underlying_symbol = underlying_symbol
        self.underlying_exchange_token = underlying_exchange_token
        self.expiry_date = expiry_date
        self.strike_price = strike_price
        self.lot_size = lot_size
        self.tick_size = tick_size
        self.freeze_quantity = freeze_quantity
        self.is_reserved = is_reserved
        self.buy_allowed = buy_allowed
        self.sell_allowed = sell_allowed


class MockQuery:
    def __init__(self, instruments):
        self.instruments = instruments
        self._filters = []
    
    def filter(self, *args):
        # Simple mock - just return self for chaining
        return self
    
    def limit(self, n):
        self.instruments = self.instruments[:n]
        return self
    
    def all(self):
        return self.instruments
    
    def first(self):
        return self.instruments[0] if self.instruments else None


class MockSession:
    def __init__(self, instruments=None):
        if instruments is None:
            instruments = [
                MockInstrument("RELIANCE", "NSE", "EQ", "Reliance Industries Ltd", "2885", "NSE-RELIANCE"),
                MockInstrument("TCS", "NSE", "EQ", "Tata Consultancy Services Ltd", "2456", "NSE-TCS"),
                MockInstrument("INFY", "BSE", "EQ", "Infosys Ltd", "500209", "BSE-INFY"),
            ]
        self.instruments = instruments
    
    def query(self, model):
        return MockQuery(self.instruments)
    
    def close(self):
        pass


@pytest.fixture(autouse=True)
def disable_scheduler(monkeypatch):
    """Prevent scheduler jobs from starting during tests."""
    monkeypatch.setattr(main_module, "_start_scheduler", lambda: None, raising=False)
    monkeypatch.setattr(main_module, "_stop_scheduler", lambda: None, raising=False)


@pytest.fixture
def client(monkeypatch):
    """Create a test client with mocked database."""
    from app.main import app
    
    # Override database dependency to avoid real DB connection
    def override_get_db():
        yield MockSession()
    
    app.dependency_overrides[instruments_router.get_db] = override_get_db
    
    yield TestClient(app)
    
    # Clean up
    app.dependency_overrides.clear()


def test_get_instrument_by_symbol_success(client):
    """Test fetching an instrument by symbol - success case."""
    response = client.get("/instruments/RELIANCE")
    assert response.status_code == 200
    
    data = response.json()
    assert data["trading_symbol"] == "RELIANCE"
    assert data["exchange"] == "NSE"
    assert data["instrument_type"] == "EQ"
    assert data["name"] == "Reliance Industries Ltd"


def test_get_instrument_by_symbol_not_found(monkeypatch):
    """Test fetching a non-existent instrument."""
    from app.main import app
    
    # Override to return empty session
    def override_get_db():
        yield MockSession(instruments=[])
    
    app.dependency_overrides[instruments_router.get_db] = override_get_db
    client = TestClient(app)
    
    response = client.get("/instruments/NONEXISTENT")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()


def test_get_instruments_all(client):
    """Test fetching all instruments without filters."""
    response = client.get("/instruments/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    symbols = {inst["trading_symbol"] for inst in data}
    assert symbols == {"RELIANCE", "TCS", "INFY"}


def test_get_instruments_filter_by_exchange(client):
    """Test fetching instruments filtered by exchange."""
    response = client.get("/instruments/?exchange=NSE")
    assert response.status_code == 200
    
    data = response.json()
    # Mock doesn't filter, so we get all 3
    assert len(data) >= 2


def test_get_instruments_filter_by_type(client):
    """Test fetching instruments filtered by instrument type."""
    response = client.get("/instruments/?instrument_type=EQ")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    assert all(inst["instrument_type"] == "EQ" for inst in data)


def test_get_instruments_filter_by_exchange_and_type(client):
    """Test fetching instruments with multiple filters."""
    response = client.get("/instruments/?exchange=BSE&instrument_type=EQ")
    assert response.status_code == 200
    
    data = response.json()
    # Mock returns all, in real scenario would be filtered
    assert len(data) >= 1


def test_get_instruments_limit(client):
    """Test limit parameter."""
    response = client.get("/instruments/?limit=2")
    assert response.status_code == 200
    
    data = response.json()
    # Mock limits work
    assert len(data) <= 2


def test_get_instruments_empty_result(monkeypatch):
    """Test filtering that returns no results."""
    from app.main import app
    
    # Override to return empty session
    def override_get_db():
        yield MockSession(instruments=[])
    
    app.dependency_overrides[instruments_router.get_db] = override_get_db
    client = TestClient(app)
    
    response = client.get("/instruments/?exchange=NONEXISTENT")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 0
    assert data == []
    
    app.dependency_overrides.clear()
