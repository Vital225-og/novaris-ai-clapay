"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.database import engine
from app.db.init_db import init_db
from app.db.seed_demo_data import seed_demo_data
from app.db.session import SessionLocal
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Novaris AI backend with modular scoring, alerts and SQLite persistence.",
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    with SessionLocal() as db:
        seed_demo_data(db)


@app.on_event("shutdown")
def shutdown_event() -> None:
    engine.dispose()
