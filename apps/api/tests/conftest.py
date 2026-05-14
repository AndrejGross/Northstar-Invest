import os
from pathlib import Path
import sys
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

API_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(API_ROOT))

from app.db.base import Base
from app.db.session import get_db
from app.models import (
    CashBalance,
    FakeTrade,
    Holding,
    Portfolio,
    PortfolioRule,
    WatchlistItem,
)
from main import app


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    pytest.exit(
        "TEST_DATABASE_URL is required for backend tests. "
        "Example: postgresql+psycopg://postgres:postgres@localhost:5432/northstar_invest_test",
        returncode=1,
    )


engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    table_names = ",".join(
        [
            "portfolio_rules",
            "fake_trades",
            "watchlist_items",
            "cash_balances",
            "holdings",
            "portfolios",
        ]
    )
    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def create_portfolio(client: TestClient):
    def _create_portfolio(name: str = "Test Portfolio", base_currency: str = "EUR"):
        response = client.post(
            "/api/portfolios",
            json={"name": name, "base_currency": base_currency},
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _create_portfolio


@pytest.fixture
def add_holding(client: TestClient):
    def _add_holding(
        portfolio_id: str,
        symbol: str = "VWCE",
        instrument_type: str = "etf",
        quantity: str = "10",
        average_cost: str = "100",
        currency: str = "EUR",
    ):
        response = client.post(
            f"/api/portfolios/{portfolio_id}/holdings",
            json={
                "symbol": symbol,
                "instrument_type": instrument_type,
                "quantity": quantity,
                "average_cost": average_cost,
                "currency": currency,
            },
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _add_holding


@pytest.fixture
def add_cash_balance(client: TestClient):
    def _add_cash_balance(
        portfolio_id: str,
        currency: str = "EUR",
        amount: str = "10000",
    ):
        response = client.post(
            f"/api/portfolios/{portfolio_id}/cash-balances",
            json={"currency": currency, "amount": amount},
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _add_cash_balance
