# Northstar Invest

Northstar Invest is a personal investing workstation for portfolio tracking, watchlists, cash balances, deterministic risk rules, and portfolio impact simulation. Invest Mode exists today; Trade Mode and Market Mode are planned as separate product areas.

## Stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLAlchemy 2.x, Pydantic
- Database: PostgreSQL
- Cache: Redis
- Migrations: Alembic
- Package manager: pnpm
- Local services: Docker Compose

## Apps

- `apps/web`: Next.js frontend
- `apps/api`: FastAPI backend

## Local Development

Install frontend dependencies:

```powershell
pnpm install
```

Start PostgreSQL and Redis:

```powershell
pnpm docker:up
```

Run database migrations:

```powershell
cd apps/api
.\.venv\Scripts\alembic.exe upgrade head
```

Install API dependencies:

```powershell
cd apps/api
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Seed demo data:

```powershell
cd apps/api
.\.venv\Scripts\python.exe scripts/seed_demo.py
```

Run backend tests:

```powershell
cd apps/api
$env:TEST_DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/northstar_invest_test"
.\.venv\Scripts\pytest.exe
```

Run the API:

```powershell
cd apps/api
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Run the web app:

```powershell
pnpm web:dev
```

## Current Backend Domains

- Portfolios
- Holdings
- Watchlist items
- Portfolio impact simulation
- Cash balances
- Portfolio summary estimates
- Portfolio rules and risk checks

## Product Modes

- Invest Mode: dashboard, portfolios, watchlist, portfolio review, Portfolio Impact Simulator, and risk rules.
- Trade Mode: planned trading simulator with charts, order tickets, long and short simulated positions, trade history, and performance statistics.
- Market Mode: planned market conditions, trend monitoring, regime detection, and symbol exploration.
- System: planned agent logs and settings.

The current simulation feature is the Portfolio Impact Simulator. It previews hypothetical portfolio actions without mutating holdings or executing orders. The future Trading Simulator is a separate module for simulated trading practice and PnL tracking.

## Notes

Portfolio values currently use local approximations such as `quantity * average_cost` and cash totals without FX conversion. Market prices and FX rates should replace those estimates in a later backend slice.
