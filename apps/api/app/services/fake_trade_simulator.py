from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.schemas.fake_trade import FakeTradeCreate, FakeTradeSimulationResult

PERCENT = Decimal("100")
TWOPLACES = Decimal("0.01")
EIGHTPLACES = Decimal("0.00000001")


def simulate_fake_trade(
    portfolio: Portfolio,
    trade_in: FakeTradeCreate,
    db: Session,
) -> FakeTradeSimulationResult:
    holding = db.scalar(
        select(Holding).where(
            Holding.portfolio_id == portfolio.id,
            Holding.symbol == trade_in.symbol,
        )
    )
    holdings = list(
        db.scalars(select(Holding).where(Holding.portfolio_id == portfolio.id)).all()
    )

    # Temporary approximation until market snapshots provide latest prices.
    estimated_portfolio_value = sum(
        (holding_item.quantity * holding_item.average_cost for holding_item in holdings),
        Decimal("0"),
    )

    before_quantity = holding.quantity if holding is not None else Decimal("0")
    before_position_value = (
        holding.quantity * holding.average_cost if holding is not None else Decimal("0")
    )
    trade_value = trade_in.quantity * trade_in.price

    if trade_in.side == "buy":
        after_quantity = before_quantity + trade_in.quantity
        after_position_value = before_position_value + trade_value
        after_portfolio_value = estimated_portfolio_value + trade_value
        total_cost_or_proceeds = trade_value + trade_in.estimated_fee
    else:
        if holding is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Cannot simulate sell: no holding exists for {trade_in.symbol}",
            )
        if trade_in.quantity > holding.quantity:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Cannot simulate sell: requested quantity exceeds current "
                    f"holding quantity of {holding.quantity}"
                ),
            )

        after_quantity = holding.quantity - trade_in.quantity
        if after_quantity == 0:
            after_position_value = Decimal("0")
        else:
            after_position_value = after_quantity * holding.average_cost
        after_portfolio_value = (
            estimated_portfolio_value - before_position_value + after_position_value
        )
        total_cost_or_proceeds = trade_value - trade_in.estimated_fee

    before_weight_pct = _calculate_weight(before_position_value, estimated_portfolio_value)
    after_weight_pct = _calculate_weight(after_position_value, after_portfolio_value)
    warnings = _build_warnings(after_weight_pct)
    summary = _build_summary(trade_in, before_quantity, after_quantity)

    return FakeTradeSimulationResult(
        trade_value=_money(trade_value),
        total_cost_or_proceeds=_money(total_cost_or_proceeds),
        before_total_position_value=_money(before_position_value),
        after_total_position_value=_money(after_position_value),
        before_position_quantity=_quantity(before_quantity),
        after_position_quantity=_quantity(after_quantity),
        before_position_weight_pct=_money(before_weight_pct),
        after_position_weight_pct=_money(after_weight_pct),
        estimated_portfolio_value=_money(after_portfolio_value),
        warnings=warnings,
        summary=summary,
    )


def _calculate_weight(position_value: Decimal, portfolio_value: Decimal) -> Decimal:
    if portfolio_value <= 0:
        return Decimal("0")
    return (position_value / portfolio_value) * PERCENT


def _build_warnings(after_weight_pct: Decimal) -> list[str]:
    warnings: list[str] = []
    if after_weight_pct > Decimal("40"):
        warnings.append(
            "Strong concentration warning: position would exceed 40% of portfolio value."
        )
    elif after_weight_pct > Decimal("25"):
        warnings.append("Concentration warning: position would exceed 25% of portfolio value.")
    return warnings


def _build_summary(
    trade_in: FakeTradeCreate,
    before_quantity: Decimal,
    after_quantity: Decimal,
) -> str:
    action = "Buy" if trade_in.side == "buy" else "Sell"
    return (
        f"{action} simulation for {trade_in.quantity} {trade_in.symbol} at "
        f"{trade_in.price} {trade_in.currency}. Quantity would change from "
        f"{before_quantity} to {after_quantity}."
    )


def _money(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def _quantity(value: Decimal) -> Decimal:
    return value.quantize(EIGHTPLACES, rounding=ROUND_HALF_UP)
