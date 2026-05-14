import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

WatchlistStatus = Literal["active", "researching", "rejected", "added"]


class WatchlistItemCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=32)
    instrument_type: str = Field(..., min_length=1, max_length=32)
    thesis: str | None = Field(default=None, max_length=2000)
    status: WatchlistStatus = "active"

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("Symbol cannot be empty")
        return normalized

    @field_validator("instrument_type")
    @classmethod
    def normalize_instrument_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("Instrument type cannot be empty")
        return normalized


class WatchlistItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    portfolio_id: uuid.UUID
    symbol: str
    instrument_type: str
    thesis: str | None
    status: str
    created_at: datetime
    updated_at: datetime
