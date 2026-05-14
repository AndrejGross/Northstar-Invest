import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

TradeSide = Literal["buy", "sell"]


class FakeTradeCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=32)
    instrument_type: str = Field(..., min_length=1, max_length=32)
    side: TradeSide
    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    estimated_fee: Decimal = Field(default=Decimal("0"), ge=0)
    notes: str | None = None

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


class FakeTradeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    portfolio_id: uuid.UUID
    symbol: str
    instrument_type: str
    side: str
    quantity: Decimal
    price: Decimal
    currency: str
    estimated_fee: Decimal
    notes: str | None
    created_at: datetime
    updated_at: datetime


class FakeTradeSimulationResult(BaseModel):
    trade_value: Decimal
    total_cost_or_proceeds: Decimal
    before_total_position_value: Decimal
    after_total_position_value: Decimal
    before_position_quantity: Decimal
    after_position_quantity: Decimal
    before_position_weight_pct: Decimal
    after_position_weight_pct: Decimal
    estimated_portfolio_value: Decimal
    warnings: list[str]
    summary: str


class FakeTradeWithSimulation(BaseModel):
    fake_trade: FakeTradeRead
    simulation: FakeTradeSimulationResult
