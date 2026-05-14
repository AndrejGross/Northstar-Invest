import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.portfolio import Portfolio
from app.models.watchlist import WatchlistItem
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemRead

router = APIRouter(tags=["watchlist"])


def get_portfolio_or_404(portfolio_id: uuid.UUID, db: Session) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.get(
    "/api/portfolios/{portfolio_id}/watchlist",
    response_model=list[WatchlistItemRead],
)
def list_watchlist_items(
    portfolio_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[WatchlistItem]:
    get_portfolio_or_404(portfolio_id, db)
    statement = (
        select(WatchlistItem)
        .where(WatchlistItem.portfolio_id == portfolio_id)
        .order_by(WatchlistItem.created_at.desc())
    )
    return list(db.scalars(statement).all())


@router.post(
    "/api/portfolios/{portfolio_id}/watchlist",
    response_model=WatchlistItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_watchlist_item(
    portfolio_id: uuid.UUID,
    item_in: WatchlistItemCreate,
    db: Session = Depends(get_db),
) -> WatchlistItem:
    get_portfolio_or_404(portfolio_id, db)
    existing_item = db.scalar(
        select(WatchlistItem).where(
            WatchlistItem.portfolio_id == portfolio_id,
            WatchlistItem.symbol == item_in.symbol,
        )
    )
    if existing_item is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Watchlist item already exists for this portfolio and symbol",
        )

    item = WatchlistItem(portfolio_id=portfolio_id, **item_in.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Watchlist item already exists for this portfolio and symbol",
        ) from None
    db.refresh(item)
    return item


@router.get("/api/watchlist/{item_id}", response_model=WatchlistItemRead)
def get_watchlist_item(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> WatchlistItem:
    item = db.get(WatchlistItem, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found",
        )
    return item


@router.delete("/api/watchlist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist_item(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Response:
    item = db.get(WatchlistItem, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found",
        )

    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
