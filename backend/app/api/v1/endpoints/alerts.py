"""Alert endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.alert_schema import AlertRecord, AlertResolveResponse
from app.services.alert_service import alert_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRecord])
def list_alerts(db: Session = Depends(get_db)) -> list[AlertRecord]:
    return alert_service.list_alerts(db)


@router.get("/{alert_id}", response_model=AlertRecord)
def get_alert(alert_id: str, db: Session = Depends(get_db)) -> AlertRecord:
    alert = alert_service.get_alert(alert_id, db)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/resolve", response_model=AlertResolveResponse)
def resolve_alert(alert_id: str, db: Session = Depends(get_db)) -> AlertResolveResponse:
    alert = alert_service.resolve_alert(alert_id, db)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
