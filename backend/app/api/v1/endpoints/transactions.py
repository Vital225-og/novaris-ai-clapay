"""Transaction analysis endpoint."""

from fastapi import APIRouter, HTTPException

from app.core.exceptions import AnalysisError
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
def analyze_transaction(payload: TransactionAnalysisRequest) -> TransactionAnalysisResponse:
    try:
        analysis = orchestrator.analyze(payload)
        stored_transaction = transaction_store.add_transaction(analysis)
        if analysis.risk_score >= 60:
            alert_service.create_alert_from_transaction(stored_transaction)
        return analysis
    except AnalysisError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[TransactionRecord])
def list_transactions() -> list[TransactionRecord]:
    return transaction_store.list_transactions()


@router.get("/{transaction_id}", response_model=TransactionRecord)
def get_transaction(transaction_id: str) -> TransactionRecord:
    transaction = transaction_store.get_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
