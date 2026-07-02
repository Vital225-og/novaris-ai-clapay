"""Dashboard endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard_schema import DashboardKPIResponse
from app.services.dashboard_service import dashboard_service

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/kpis", response_model=DashboardKPIResponse)
def get_dashboard_kpis(db: Session = Depends(get_db)) -> DashboardKPIResponse:
    return dashboard_service.get_kpis(db)
