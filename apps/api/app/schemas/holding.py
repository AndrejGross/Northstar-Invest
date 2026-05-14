import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HoldingCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=32)
    instrument_type: str = Field(..., min_length=1, max_length=32)
    quantity: Decimal = Field(..., gt=0)
    average_cost: Decimal = Field(..., ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    notes: str | None = None

    @field_validator("symbol", "currency")
    @classmethod
    def normalize_uppercase(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("Value cannot be empty")
        return normalized

    @field_validator("instrument_type")
    @classmethod
    def normalize_instrument_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("Instrument type cannot be empty")
        return normalized


class HoldingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    portfolio_id: uuid.UUID
    symbol: str
    instrument_type: str
    quantity: Decimal
    average_cost: Decimal
    currency: str
    notes: str | None
    created_at: datetime
    updated_at: datetime
