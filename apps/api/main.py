from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import fake_trades, health, holdings, portfolios, watchlist
from app.core.config import get_settings

settings = get_settings()

# Database schema is managed by Alembic. Run `alembic upgrade head` before serving.
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(portfolios.router)
app.include_router(holdings.router)
app.include_router(watchlist.router)
app.include_router(fake_trades.router)


@app.get("/")
def root():
    return {"name": settings.app_name, "environment": settings.app_env}
