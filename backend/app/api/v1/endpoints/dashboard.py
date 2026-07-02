"""Dashboard endpoints."""

from fastapi import APIRouter

from app.schemas.dashboard_schema import DashboardKPIResponse
from app.services.dashboard_service import dashboard_service

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/kpis", response_model=DashboardKPIResponse)
def get_dashboard_kpis() -> DashboardKPIResponse:
    return dashboard_service.get_kpis()

