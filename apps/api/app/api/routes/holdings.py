import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.schemas.holding import HoldingCreate, HoldingRead

router = APIRouter(tags=["holdings"])


def get_portfolio_or_404(portfolio_id: uuid.UUID, db: Session) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.get(
    "/api/portfolios/{portfolio_id}/holdings",
    response_model=list[HoldingRead],
)
def list_holdings(
    portfolio_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[Holding]:
    get_portfolio_or_404(portfolio_id, db)
    statement = (
        select(Holding)
        .where(Holding.portfolio_id == portfolio_id)
        .order_by(Holding.created_at.desc())
    )
    return list(db.scalars(statement).all())


@router.post(
    "/api/portfolios/{portfolio_id}/holdings",
    response_model=HoldingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_holding(
    portfolio_id: uuid.UUID,
    holding_in: HoldingCreate,
    db: Session = Depends(get_db),
) -> Holding:
    get_portfolio_or_404(portfolio_id, db)
    existing_holding = db.scalar(
        select(Holding).where(
            Holding.portfolio_id == portfolio_id,
            Holding.symbol == holding_in.symbol,
        )
    )
    if existing_holding is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Holding already exists for this portfolio and symbol",
        )

    holding = Holding(portfolio_id=portfolio_id, **holding_in.model_dump())
    db.add(holding)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Holding already exists for this portfolio and symbol",
        ) from None
    db.refresh(holding)
    return holding


@router.get("/api/holdings/{holding_id}", response_model=HoldingRead)
def get_holding(
    holding_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Holding:
    holding = db.get(Holding, holding_id)
    if holding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found",
        )
    return holding


@router.delete("/api/holdings/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holding(
    holding_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Response:
    holding = db.get(Holding, holding_id)
    if holding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found",
        )

    db.delete(holding)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
