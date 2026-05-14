from decimal import Decimal
from pathlib import Path
import sys

from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.cash_balance import CashBalance
from app.models.fake_trade import FakeTrade
from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.models.portfolio_rule import PortfolioRule
from app.models.watchlist import WatchlistItem

DEMO_PORTFOLIO_NAME = "Demo Growth Portfolio"


def main() -> None:
    db = SessionLocal()
    try:
        existing_portfolios = list(
            db.scalars(
                select(Portfolio).where(Portfolio.name == DEMO_PORTFOLIO_NAME)
            ).all()
        )
        for portfolio in existing_portfolios:
            db.delete(portfolio)
        db.commit()

        portfolio = Portfolio(name=DEMO_PORTFOLIO_NAME, base_currency="EUR")
        db.add(portfolio)
        db.flush()

        cash_balances = [
            CashBalance(portfolio_id=portfolio.id, currency="EUR", amount=Decimal("10000")),
            CashBalance(portfolio_id=portfolio.id, currency="USD", amount=Decimal("5000")),
        ]
        holdings = [
            Holding(
                portfolio_id=portfolio.id,
                symbol="AAPL",
                instrument_type="stock",
                quantity=Decimal("10"),
                average_cost=Decimal("180"),
                currency="USD",
            ),
            Holding(
                portfolio_id=portfolio.id,
                symbol="MSFT",
                instrument_type="stock",
                quantity=Decimal("8"),
                average_cost=Decimal("320"),
                currency="USD",
            ),
            Holding(
                portfolio_id=portfolio.id,
                symbol="VWCE",
                instrument_type="etf",
                quantity=Decimal("20"),
                average_cost=Decimal("105"),
                currency="EUR",
            ),
            Holding(
                portfolio_id=portfolio.id,
                symbol="SXR8",
                instrument_type="etf",
                quantity=Decimal("5"),
                average_cost=Decimal("500"),
                currency="EUR",
            ),
        ]
        watchlist_items = [
            WatchlistItem(
                portfolio_id=portfolio.id,
                symbol="NVDA",
                instrument_type="stock",
                status="researching",
            ),
            WatchlistItem(
                portfolio_id=portfolio.id,
                symbol="SPY",
                instrument_type="etf",
                status="active",
            ),
            WatchlistItem(
                portfolio_id=portfolio.id,
                symbol="QQQ",
                instrument_type="etf",
                status="active",
            ),
        ]
        portfolio_rule = PortfolioRule(
            portfolio_id=portfolio.id,
            max_single_position_pct=Decimal("25"),
            max_stock_position_pct=Decimal("20"),
            max_etf_position_pct=Decimal("40"),
            min_cash_reserve_pct=Decimal("5"),
            concentration_warning_pct=Decimal("20"),
            concentration_danger_pct=Decimal("35"),
            allowed_currencies=["EUR", "USD"],
            blocked_symbols=["TSLA"],
        )
        fake_trades = [
            FakeTrade(
                portfolio_id=portfolio.id,
                symbol="VWCE",
                instrument_type="etf",
                side="buy",
                quantity=Decimal("5"),
                price=Decimal("110"),
                currency="EUR",
                estimated_fee=Decimal("1.5"),
                notes="Demo recurring buy idea",
            ),
            FakeTrade(
                portfolio_id=portfolio.id,
                symbol="AAPL",
                instrument_type="stock",
                side="sell",
                quantity=Decimal("2"),
                price=Decimal("195"),
                currency="USD",
                estimated_fee=Decimal("1"),
                notes="Demo trim scenario",
            ),
        ]

        db.add_all(cash_balances)
        db.add_all(holdings)
        db.add_all(watchlist_items)
        db.add(portfolio_rule)
        db.add_all(fake_trades)
        db.commit()

        print("Demo data seeded")
        print(f"portfolio_id={portfolio.id}")
        print(f"cash_balances={len(cash_balances)}")
        print(f"holdings={len(holdings)}")
        print(f"watchlist_items={len(watchlist_items)}")
        print(f"fake_trades={len(fake_trades)}")
        print("portfolio_rules=1")
    finally:
        db.close()


if __name__ == "__main__":
    main()
