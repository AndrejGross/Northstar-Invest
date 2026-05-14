from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cash_balance import CashBalance
from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.schemas.cash_balance import (
    PortfolioAllocationItem,
    PortfolioPositionSummary,
    PortfolioSummaryRead,
)

PERCENT = Decimal("100")
TWOPLACES = Decimal("0.01")
EIGHTPLACES = Decimal("0.00000001")


def build_portfolio_summary(
    portfolio: Portfolio,
    db: Session,
) -> PortfolioSummaryRead:
    holdings = list(
        db.scalars(select(Holding).where(Holding.portfolio_id == portfolio.id)).all()
    )
    cash_balances = list(
        db.scalars(
            select(CashBalance).where(CashBalance.portfolio_id == portfolio.id)
        ).all()
    )

    # Temporary estimates until market prices and FX rates are available.
    holding_values = [
        (holding, holding.quantity * holding.average_cost) for holding in holdings
    ]
    holdings_value = sum((value for _, value in holding_values), Decimal("0"))
    cash_total = sum((cash.amount for cash in cash_balances), Decimal("0"))
    total_value = holdings_value + cash_total

    ordered_positions = sorted(
        holding_values,
        key=lambda item: item[1],
        reverse=True,
    )
    top_positions = [
        PortfolioPositionSummary(
            symbol=holding.symbol,
            instrument_type=holding.instrument_type,
            quantity=_quantity(holding.quantity),
            estimated_value=_money(value),
            allocation_pct=_money(_allocation_pct(value, total_value)),
        )
        for holding, value in ordered_positions[:5]
    ]
    allocation_by_symbol = [
        PortfolioAllocationItem(
            symbol=holding.symbol,
            estimated_value=_money(value),
            allocation_pct=_money(_allocation_pct(value, total_value)),
        )
        for holding, value in ordered_positions
    ]

    warnings = _build_warnings(portfolio, holdings, cash_balances)

    return PortfolioSummaryRead(
        portfolio_id=portfolio.id,
        portfolio_name=portfolio.name,
        base_currency=portfolio.base_currency,
        holdings_value_estimate=_money(holdings_value),
        cash_total_estimate=_money(cash_total),
        total_value_estimate=_money(total_value),
        holdings_count=len(holdings),
        cash_balances_count=len(cash_balances),
        top_positions=top_positions,
        allocation_by_symbol=allocation_by_symbol,
        warnings=warnings,
    )


def _allocation_pct(value: Decimal, total_value: Decimal) -> Decimal:
    if total_value <= 0:
        return Decimal("0")
    return (value / total_value) * PERCENT


def _build_warnings(
    portfolio: Portfolio,
    holdings: list[Holding],
    cash_balances: list[CashBalance],
) -> list[str]:
    currencies = {portfolio.base_currency}
    currencies.update(holding.currency for holding in holdings)
    currencies.update(cash.currency for cash in cash_balances)

    if len(currencies) > 1:
        return [
            "Cross-currency totals are approximate until FX conversion is implemented."
        ]
    return []


def _money(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def _quantity(value: Decimal) -> Decimal:
    return value.quantize(EIGHTPLACES, rounding=ROUND_HALF_UP)
