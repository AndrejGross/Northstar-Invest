import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.cash_balance import CashBalance
from app.models.portfolio import Portfolio
from app.schemas.cash_balance import (
    CashBalanceCreate,
    CashBalanceRead,
    CashBalanceUpdate,
    PortfolioSummaryRead,
)
from app.services.portfolio_summary import build_portfolio_summary

router = APIRouter(tags=["cash balances"])


def get_portfolio_or_404(portfolio_id: uuid.UUID, db: Session) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.get(
    "/api/portfolios/{portfolio_id}/cash-balances",
    response_model=list[CashBalanceRead],
)
def list_cash_balances(
    portfolio_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[CashBalance]:
    get_portfolio_or_404(portfolio_id, db)
    statement = (
        select(CashBalance)
        .where(CashBalance.portfolio_id == portfolio_id)
        .order_by(CashBalance.created_at.desc())
    )
    return list(db.scalars(statement).all())


@router.post(
    "/api/portfolios/{portfolio_id}/cash-balances",
    response_model=CashBalanceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_cash_balance(
    portfolio_id: uuid.UUID,
    cash_balance_in: CashBalanceCreate,
    db: Session = Depends(get_db),
) -> CashBalance:
    get_portfolio_or_404(portfolio_id, db)
    existing_balance = db.scalar(
        select(CashBalance).where(
            CashBalance.portfolio_id == portfolio_id,
            CashBalance.currency == cash_balance_in.currency,
        )
    )
    if existing_balance is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cash balance already exists for this portfolio and currency",
        )

    cash_balance = CashBalance(
        portfolio_id=portfolio_id,
        **cash_balance_in.model_dump(),
    )
    db.add(cash_balance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cash balance already exists for this portfolio and currency",
        ) from None
    db.refresh(cash_balance)
    return cash_balance


@router.get("/api/cash-balances/{cash_balance_id}", response_model=CashBalanceRead)
def get_cash_balance(
    cash_balance_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> CashBalance:
    cash_balance = db.get(CashBalance, cash_balance_id)
    if cash_balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cash balance not found",
        )
    return cash_balance


@router.patch("/api/cash-balances/{cash_balance_id}", response_model=CashBalanceRead)
def update_cash_balance(
    cash_balance_id: uuid.UUID,
    cash_balance_in: CashBalanceUpdate,
    db: Session = Depends(get_db),
) -> CashBalance:
    cash_balance = db.get(CashBalance, cash_balance_id)
    if cash_balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cash balance not found",
        )

    cash_balance.amount = cash_balance_in.amount
    db.commit()
    db.refresh(cash_balance)
    return cash_balance


@router.delete(
    "/api/cash-balances/{cash_balance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_cash_balance(
    cash_balance_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Response:
    cash_balance = db.get(CashBalance, cash_balance_id)
    if cash_balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cash balance not found",
        )

    db.delete(cash_balance)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/api/portfolios/{portfolio_id}/summary",
    response_model=PortfolioSummaryRead,
)
def get_portfolio_summary(
    portfolio_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> PortfolioSummaryRead:
    portfolio = get_portfolio_or_404(portfolio_id, db)
    return build_portfolio_summary(portfolio, db)
