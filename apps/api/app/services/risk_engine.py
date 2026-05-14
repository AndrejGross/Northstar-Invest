from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cash_balance import CashBalance
from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.models.portfolio_rule import PortfolioRule
from app.schemas.portfolio_rule import (
    PortfolioRuleRead,
    RiskCheckInput,
    RiskCheckResult,
    RiskMetrics,
)

PERCENT = Decimal("100")
TWOPLACES = Decimal("0.01")


def get_saved_or_default_rules(
    portfolio: Portfolio,
    db: Session,
) -> PortfolioRuleRead:
    saved_rule = db.scalar(
        select(PortfolioRule).where(PortfolioRule.portfolio_id == portfolio.id)
    )
    if saved_rule is not None:
        return PortfolioRuleRead.model_validate(saved_rule)

    return PortfolioRuleRead(
        portfolio_id=portfolio.id,
        is_default=True,
    )


def run_risk_check(
    portfolio: Portfolio,
    trade_in: RiskCheckInput,
    db: Session,
) -> RiskCheckResult:
    rules = get_saved_or_default_rules(portfolio, db)
    holdings = list(
        db.scalars(select(Holding).where(Holding.portfolio_id == portfolio.id)).all()
    )
    cash_balances = list(
        db.scalars(
            select(CashBalance).where(CashBalance.portfolio_id == portfolio.id)
        ).all()
    )

    holding = next(
        (item for item in holdings if item.symbol == trade_in.symbol),
        None,
    )
    cash_for_currency = next(
        (item for item in cash_balances if item.currency == trade_in.currency),
        None,
    )

    holdings_value = sum(
        (item.quantity * item.average_cost for item in holdings),
        Decimal("0"),
    )
    cash_total = sum((item.amount for item in cash_balances), Decimal("0"))
    trade_value = trade_in.quantity * trade_in.price
    cash_delta = _cash_delta(trade_in, trade_value)
    current_currency_cash = (
        cash_for_currency.amount if cash_for_currency is not None else Decimal("0")
    )
    estimated_cash_after_trade = current_currency_cash + cash_delta

    current_position_value = (
        holding.quantity * holding.average_cost if holding is not None else Decimal("0")
    )
    after_position_value = _after_position_value(holding, trade_in, trade_value)
    after_holdings_value = holdings_value - current_position_value + after_position_value
    after_cash_total = cash_total + cash_delta
    estimated_total_value = after_holdings_value + after_cash_total
    after_position_weight_pct = _pct(after_position_value, estimated_total_value)
    after_cash_pct = _pct(after_cash_total, estimated_total_value)
    min_cash_required = estimated_total_value * rules.min_cash_reserve_pct / PERCENT

    violations: list[str] = []
    warnings: list[str] = []

    _check_symbol_rules(trade_in, rules, violations)
    _check_currency_rules(trade_in, rules, warnings)
    _check_cash_rules(
        trade_in,
        estimated_cash_after_trade,
        after_cash_total,
        min_cash_required,
        rules,
        violations,
        warnings,
    )
    _check_sell_rules(trade_in, holding, violations)
    _check_concentration_rules(
        trade_in,
        after_position_weight_pct,
        rules,
        violations,
        warnings,
    )

    risk_level = _risk_level(violations, warnings, after_position_weight_pct, rules)
    allowed = not violations

    return RiskCheckResult(
        allowed=allowed,
        risk_level=risk_level,
        violations=violations,
        warnings=warnings,
        metrics=RiskMetrics(
            estimated_total_value=_money(estimated_total_value),
            estimated_cash_after_trade=_money(estimated_cash_after_trade),
            after_position_weight_pct=_money(after_position_weight_pct),
            min_cash_required=_money(min_cash_required),
            after_cash_pct=_money(after_cash_pct),
        ),
        summary=_summary(trade_in, allowed, risk_level),
    )


def _cash_delta(trade_in: RiskCheckInput, trade_value: Decimal) -> Decimal:
    if trade_in.side == "buy":
        return -(trade_value + trade_in.estimated_fee)
    return trade_value - trade_in.estimated_fee


def _after_position_value(
    holding: Holding | None,
    trade_in: RiskCheckInput,
    trade_value: Decimal,
) -> Decimal:
    current_value = (
        holding.quantity * holding.average_cost if holding is not None else Decimal("0")
    )
    if trade_in.side == "buy":
        return current_value + trade_value
    if holding is None:
        return Decimal("0")

    after_quantity = holding.quantity - trade_in.quantity
    if after_quantity <= 0:
        return Decimal("0")
    return after_quantity * holding.average_cost


def _check_symbol_rules(
    trade_in: RiskCheckInput,
    rules: PortfolioRuleRead,
    violations: list[str],
) -> None:
    if rules.blocked_symbols and trade_in.symbol in rules.blocked_symbols:
        violations.append(f"{trade_in.symbol} is blocked by portfolio rules.")


def _check_currency_rules(
    trade_in: RiskCheckInput,
    rules: PortfolioRuleRead,
    warnings: list[str],
) -> None:
    if rules.allowed_currencies and trade_in.currency not in rules.allowed_currencies:
        warnings.append(
            f"{trade_in.currency} is not in allowed_currencies for this portfolio."
        )


def _check_cash_rules(
    trade_in: RiskCheckInput,
    estimated_cash_after_trade: Decimal,
    after_cash_total: Decimal,
    min_cash_required: Decimal,
    rules: PortfolioRuleRead,
    violations: list[str],
    warnings: list[str],
) -> None:
    if trade_in.side == "buy" and estimated_cash_after_trade < 0:
        violations.append(
            f"Insufficient {trade_in.currency} cash for this simulated buy."
        )
    if after_cash_total < min_cash_required:
        warnings.append(
            "Cash reserve would fall below "
            f"{rules.min_cash_reserve_pct}% of estimated portfolio value."
        )


def _check_sell_rules(
    trade_in: RiskCheckInput,
    holding: Holding | None,
    violations: list[str],
) -> None:
    if trade_in.side != "sell":
        return
    if holding is None:
        violations.append(f"Cannot sell {trade_in.symbol}: no holding exists.")
        return
    if trade_in.quantity > holding.quantity:
        violations.append(
            "Cannot sell more than current holding quantity "
            f"({holding.quantity})."
        )


def _check_concentration_rules(
    trade_in: RiskCheckInput,
    after_position_weight_pct: Decimal,
    rules: PortfolioRuleRead,
    violations: list[str],
    warnings: list[str],
) -> None:
    if after_position_weight_pct > rules.max_single_position_pct:
        violations.append(
            "Position would exceed max_single_position_pct "
            f"({rules.max_single_position_pct}%)."
        )
    if (
        trade_in.instrument_type == "stock"
        and after_position_weight_pct > rules.max_stock_position_pct
    ):
        violations.append(
            f"Stock position would exceed {rules.max_stock_position_pct}% limit."
        )
    if (
        trade_in.instrument_type == "etf"
        and after_position_weight_pct > rules.max_etf_position_pct
    ):
        violations.append(
            f"ETF position would exceed {rules.max_etf_position_pct}% limit."
        )
    if after_position_weight_pct > rules.concentration_danger_pct:
        violations.append(
            "Position concentration would exceed danger threshold "
            f"({rules.concentration_danger_pct}%)."
        )
    elif after_position_weight_pct > rules.concentration_warning_pct:
        warnings.append(
            "Position concentration would exceed warning threshold "
            f"({rules.concentration_warning_pct}%)."
        )


def _risk_level(
    violations: list[str],
    warnings: list[str],
    after_position_weight_pct: Decimal,
    rules: PortfolioRuleRead,
) -> str:
    if violations:
        return "blocked"
    if after_position_weight_pct > rules.concentration_danger_pct:
        return "high"
    if warnings:
        return "medium"
    return "low"


def _summary(trade_in: RiskCheckInput, allowed: bool, risk_level: str) -> str:
    outcome = "allowed" if allowed else "blocked"
    return (
        f"{trade_in.side.title()} risk check for {trade_in.quantity} "
        f"{trade_in.symbol} is {outcome} with {risk_level} risk."
    )


def _pct(value: Decimal, total: Decimal) -> Decimal:
    if total <= 0:
        return Decimal("0")
    return value / total * PERCENT


def _money(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
