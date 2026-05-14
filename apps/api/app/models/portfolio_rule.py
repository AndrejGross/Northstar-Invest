import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio


class PortfolioRule(Base):
    __tablename__ = "portfolio_rules"
    __table_args__ = (
        UniqueConstraint("portfolio_id", name="uq_portfolio_rules_portfolio_id"),
        CheckConstraint(
            "max_single_position_pct >= 0 AND max_single_position_pct <= 100",
            name="ck_portfolio_rules_max_single_position_pct_range",
        ),
        CheckConstraint(
            "max_stock_position_pct >= 0 AND max_stock_position_pct <= 100",
            name="ck_portfolio_rules_max_stock_position_pct_range",
        ),
        CheckConstraint(
            "max_etf_position_pct >= 0 AND max_etf_position_pct <= 100",
            name="ck_portfolio_rules_max_etf_position_pct_range",
        ),
        CheckConstraint(
            "min_cash_reserve_pct >= 0 AND min_cash_reserve_pct <= 100",
            name="ck_portfolio_rules_min_cash_reserve_pct_range",
        ),
        CheckConstraint(
            "concentration_warning_pct >= 0 AND concentration_warning_pct <= 100",
            name="ck_portfolio_rules_concentration_warning_pct_range",
        ),
        CheckConstraint(
            "concentration_danger_pct >= 0 AND concentration_danger_pct <= 100",
            name="ck_portfolio_rules_concentration_danger_pct_range",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    max_single_position_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("25"),
    )
    max_stock_position_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("20"),
    )
    max_etf_position_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("40"),
    )
    min_cash_reserve_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("5"),
    )
    concentration_warning_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("25"),
    )
    concentration_danger_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("40"),
    )
    allowed_currencies: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    blocked_symbols: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="rule")
