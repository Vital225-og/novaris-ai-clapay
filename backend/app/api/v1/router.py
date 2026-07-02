"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints.alerts import router as alerts_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.transactions import router as transactions_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(dashboard_router)
api_router.include_router(alerts_router)
api_router.include_router(transactions_router)
