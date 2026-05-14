# Northstar Invest API

FastAPI backend for Northstar Invest.

## Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

or:

```powershell
fastapi dev main.py
```

## Database Migrations

Alembic reads `DATABASE_URL` through `app.core.config`. Set the same environment variables used by the API before running migrations.

```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/northstar_invest"
```

Apply all migrations:

```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

Downgrade one revision:

```powershell
.\.venv\Scripts\alembic.exe downgrade -1
```

Generate a new migration after changing SQLAlchemy models:

```powershell
.\.venv\Scripts\alembic.exe revision --autogenerate -m "describe_schema_change"
```

If the API virtualenv is activated and PowerShell can resolve the local scripts directory, this shorter form also works:

```powershell
alembic upgrade head
```

Review generated migrations before applying them.

## Seed Demo Data

Run migrations first, then seed the demo portfolio:

```powershell
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe scripts/seed_demo.py
```

The seed script safely resets only the `Demo Growth Portfolio` data.

## Tests

Tests require an isolated PostgreSQL database. Create one locally, then set `TEST_DATABASE_URL` before running pytest.

```powershell
$env:TEST_DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/northstar_invest_test"
.\.venv\Scripts\pytest.exe
```

The test harness recreates tables in the test database and truncates data between tests.
