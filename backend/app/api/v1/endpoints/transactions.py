"""Transaction analysis endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import AnalysisError
from app.db.session import get_db
from app.schemas.transaction_schema import (
    TransactionAnalysisRequest,
    TransactionAnalysisResponse,
    TransactionRecord,
)
from app.services.alert_service import alert_service
from app.services.risk_orchestrator import RiskOrchestrator
from app.services.transaction_store import transaction_store

router = APIRouter(prefix="/transactions", tags=["transactions"])

orchestrator = RiskOrchestrator()


@router.post("/analyze", response_model=TransactionAnalysisResponse)
def analyze_transaction(
    payload: TransactionAnalysisRequest,
    db: Session = Depends(get_db),
) -> TransactionAnalysisResponse:
    try:
        analysis = orchestrator.analyze(payload)
        stored_transaction = transaction_store.add_transaction(db, payload, analysis)
        if analysis.risk_score >= 60:
            alert_service.create_alert_from_transaction(db, stored_transaction)
        return analysis
    except AnalysisError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[TransactionRecord])
def list_transactions(db: Session = Depends(get_db)) -> list[TransactionRecord]:
    return transaction_store.list_transactions(db)


@router.get("/{transaction_id}", response_model=TransactionRecord)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)) -> TransactionRecord:
    transaction = transaction_store.get_transaction(transaction_id, db)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
