import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

RiskLevel = Literal["low", "medium", "high", "blocked"]
TradeSide = Literal["buy", "sell"]


class PortfolioRuleBase(BaseModel):
    max_single_position_pct: Decimal = Field(default=Decimal("25"), ge=0, le=100)
    max_stock_position_pct: Decimal = Field(default=Decimal("20"), ge=0, le=100)
    max_etf_position_pct: Decimal = Field(default=Decimal("40"), ge=0, le=100)
    min_cash_reserve_pct: Decimal = Field(default=Decimal("5"), ge=0, le=100)
    concentration_warning_pct: Decimal = Field(default=Decimal("25"), ge=0, le=100)
    concentration_danger_pct: Decimal = Field(default=Decimal("40"), ge=0, le=100)
    allowed_currencies: list[str] | None = None
    blocked_symbols: list[str] | None = None

    @field_validator("allowed_currencies", "blocked_symbols", mode="before")
    @classmethod
    def normalize_optional_uppercase_list(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        if value is None:
            return None
        normalized = []
        for item in value:
            cleaned = item.strip().upper()
            if cleaned:
                normalized.append(cleaned)
        return sorted(set(normalized))


class PortfolioRuleUpdate(PortfolioRuleBase):
    pass


class PortfolioRuleRead(PortfolioRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = None
    portfolio_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_default: bool = False


class RiskCheckInput(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=32)
    instrument_type: str = Field(..., min_length=1, max_length=32)
    side: TradeSide
    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    estimated_fee: Decimal = Field(default=Decimal("0"), ge=0)

    @field_validator("symbol", "currency", mode="before")
    @classmethod
    def normalize_uppercase(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("Value cannot be empty")
        return normalized

    @field_validator("instrument_type", "side", mode="before")
    @classmethod
    def normalize_lowercase(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("Value cannot be empty")
        return normalized


class RiskMetrics(BaseModel):
    estimated_total_value: Decimal
    estimated_cash_after_trade: Decimal
    after_position_weight_pct: Decimal
    min_cash_required: Decimal
    after_cash_pct: Decimal


class RiskCheckResult(BaseModel):
    allowed: bool
    risk_level: RiskLevel
    violations: list[str]
    warnings: list[str]
    metrics: RiskMetrics
    summary: str
