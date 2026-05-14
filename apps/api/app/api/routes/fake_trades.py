import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.fake_trade import FakeTrade
from app.models.portfolio import Portfolio
from app.schemas.fake_trade import (
    FakeTradeCreate,
    FakeTradeRead,
    FakeTradeSimulationResult,
    FakeTradeWithSimulation,
)
from app.services.fake_trade_simulator import simulate_fake_trade

router = APIRouter(tags=["fake trades"])


def get_portfolio_or_404(portfolio_id: uuid.UUID, db: Session) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.post(
    "/api/portfolios/{portfolio_id}/fake-trades/preview",
    response_model=FakeTradeSimulationResult,
)
def preview_fake_trade(
    portfolio_id: uuid.UUID,
    trade_in: FakeTradeCreate,
    db: Session = Depends(get_db),
) -> FakeTradeSimulationResult:
    portfolio = get_portfolio_or_404(portfolio_id, db)
    return simulate_fake_trade(portfolio, trade_in, db)


@router.post(
    "/api/portfolios/{portfolio_id}/fake-trades",
    response_model=FakeTradeWithSimulation,
    status_code=status.HTTP_201_CREATED,
)
def create_fake_trade(
    portfolio_id: uuid.UUID,
    trade_in: FakeTradeCreate,
    db: Session = Depends(get_db),
) -> FakeTradeWithSimulation:
    portfolio = get_portfolio_or_404(portfolio_id, db)
    simulation = simulate_fake_trade(portfolio, trade_in, db)

    fake_trade = FakeTrade(portfolio_id=portfolio_id, **trade_in.model_dump())
    db.add(fake_trade)
    db.commit()
    db.refresh(fake_trade)

    return FakeTradeWithSimulation(fake_trade=fake_trade, simulation=simulation)


@router.get(
    "/api/portfolios/{portfolio_id}/fake-trades",
    response_model=list[FakeTradeRead],
)
def list_fake_trades(
    portfolio_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[FakeTrade]:
    get_portfolio_or_404(portfolio_id, db)
    statement = (
        select(FakeTrade)
        .where(FakeTrade.portfolio_id == portfolio_id)
        .order_by(FakeTrade.created_at.desc())
    )
    return list(db.scalars(statement).all())


@router.get("/api/fake-trades/{fake_trade_id}", response_model=FakeTradeRead)
def get_fake_trade(
    fake_trade_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> FakeTrade:
    fake_trade = db.get(FakeTrade, fake_trade_id)
    if fake_trade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fake trade not found",
        )
    return fake_trade


@router.delete(
    "/api/fake-trades/{fake_trade_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_fake_trade(
    fake_trade_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Response:
    fake_trade = db.get(FakeTrade, fake_trade_id)
    if fake_trade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fake trade not found",
        )

    db.delete(fake_trade)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
