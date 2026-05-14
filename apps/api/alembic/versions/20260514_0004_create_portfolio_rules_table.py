"""create portfolio rules table

Revision ID: 20260514_0004
Revises: 20260514_0003
Create Date: 2026-05-14 00:00:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260514_0004"
down_revision: str | None = "20260514_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "portfolio_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("portfolio_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "max_single_position_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "max_stock_position_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "max_etf_position_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "min_cash_reserve_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "concentration_warning_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "concentration_danger_pct",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column("allowed_currencies", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("blocked_symbols", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "max_single_position_pct >= 0 AND max_single_position_pct <= 100",
            name="ck_portfolio_rules_max_single_position_pct_range",
        ),
        sa.CheckConstraint(
            "max_stock_position_pct >= 0 AND max_stock_position_pct <= 100",
            name="ck_portfolio_rules_max_stock_position_pct_range",
        ),
        sa.CheckConstraint(
            "max_etf_position_pct >= 0 AND max_etf_position_pct <= 100",
            name="ck_portfolio_rules_max_etf_position_pct_range",
        ),
        sa.CheckConstraint(
            "min_cash_reserve_pct >= 0 AND min_cash_reserve_pct <= 100",
            name="ck_portfolio_rules_min_cash_reserve_pct_range",
        ),
        sa.CheckConstraint(
            "concentration_warning_pct >= 0 AND concentration_warning_pct <= 100",
            name="ck_portfolio_rules_concentration_warning_pct_range",
        ),
        sa.CheckConstraint(
            "concentration_danger_pct >= 0 AND concentration_danger_pct <= 100",
            name="ck_portfolio_rules_concentration_danger_pct_range",
        ),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("portfolio_id", name="uq_portfolio_rules_portfolio_id"),
    )
    op.create_index(
        op.f("ix_portfolio_rules_portfolio_id"),
        "portfolio_rules",
        ["portfolio_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_portfolio_rules_portfolio_id"), table_name="portfolio_rules")
    op.drop_table("portfolio_rules")
