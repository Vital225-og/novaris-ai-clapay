"""Transaction analysis endpoint."""

from fastapi import APIRouter, HTTPException

from app.core.exceptions import AnalysisError
from app.schemas.transaction_schema import TransactionAnalysisRequest, TransactionAnalysisResponse
from app.services.risk_orchestrator import RiskOrchestrator

router = APIRouter(prefix="/transactions", tags=["transactions"])

orchestrator = RiskOrchestrator()


@router.post("/analyze", response_model=TransactionAnalysisResponse)
def analyze_transaction(payload: TransactionAnalysisRequest) -> TransactionAnalysisResponse:
    try:
        return orchestrator.analyze(payload)
    except AnalysisError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

