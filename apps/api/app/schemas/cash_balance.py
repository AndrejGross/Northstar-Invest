import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CashBalanceCreate(BaseModel):
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    amount: Decimal = Field(..., ge=0)

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("Currency cannot be empty")
        return normalized


class CashBalanceUpdate(BaseModel):
    amount: Decimal = Field(..., ge=0)


class CashBalanceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    portfolio_id: uuid.UUID
    currency: str
    amount: Decimal
    created_at: datetime
    updated_at: datetime


class PortfolioPositionSummary(BaseModel):
    symbol: str
    instrument_type: str
    quantity: Decimal
    estimated_value: Decimal
    allocation_pct: Decimal


class PortfolioAllocationItem(BaseModel):
    symbol: str
    estimated_value: Decimal
    allocation_pct: Decimal


class PortfolioSummaryRead(BaseModel):
    portfolio_id: uuid.UUID
    portfolio_name: str
    base_currency: str
    holdings_value_estimate: Decimal
    cash_total_estimate: Decimal
    total_value_estimate: Decimal
    holdings_count: int
    cash_balances_count: int
    top_positions: list[PortfolioPositionSummary]
    allocation_by_symbol: list[PortfolioAllocationItem]
    warnings: list[str]
