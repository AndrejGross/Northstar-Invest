import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.portfolio import Portfolio
from app.models.portfolio_rule import PortfolioRule
from app.schemas.portfolio_rule import (
    PortfolioRuleRead,
    PortfolioRuleUpdate,
    RiskCheckInput,
    RiskCheckResult,
)
from app.services.risk_engine import get_saved_or_default_rules, run_risk_check

router = APIRouter(tags=["portfolio rules"])


def get_portfolio_or_404(portfolio_id: uuid.UUID, db: Session) -> Portfolio:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    return portfolio


@router.get("/api/portfolios/{portfolio_id}/rules", response_model=PortfolioRuleRead)
def get_portfolio_rules(
    portfolio_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> PortfolioRuleRead:
    portfolio = get_portfolio_or_404(portfolio_id, db)
    return get_saved_or_default_rules(portfolio, db)


@router.put("/api/portfolios/{portfolio_id}/rules", response_model=PortfolioRuleRead)
def upsert_portfolio_rules(
    portfolio_id: uuid.UUID,
    rules_in: PortfolioRuleUpdate,
    db: Session = Depends(get_db),
) -> PortfolioRule:
    get_portfolio_or_404(portfolio_id, db)
    rule = db.scalar(
        select(PortfolioRule).where(PortfolioRule.portfolio_id == portfolio_id)
    )
    if rule is None:
        rule = PortfolioRule(portfolio_id=portfolio_id)
        db.add(rule)

    for field, value in rules_in.model_dump().items():
        setattr(rule, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Portfolio rules already exist for this portfolio",
        ) from None
    db.refresh(rule)
    return rule


@router.post(
    "/api/portfolios/{portfolio_id}/risk-check",
    response_model=RiskCheckResult,
)
def check_portfolio_risk(
    portfolio_id: uuid.UUID,
    trade_in: RiskCheckInput,
    db: Session = Depends(get_db),
) -> RiskCheckResult:
    portfolio = get_portfolio_or_404(portfolio_id, db)
    return run_risk_check(portfolio, trade_in, db)
