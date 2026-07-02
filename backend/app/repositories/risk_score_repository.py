"""Risk score repository."""

import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.risk_score import RiskScore
from app.schemas.transaction_schema import TransactionAnalysisResponse


def create_risk_score(db: Session, analysis_result: TransactionAnalysisResponse) -> RiskScore:
    risk_score = RiskScore(
        transaction_id=analysis_result.transaction_id,
        transaction_monitoring_score=analysis_result.module_scores.transaction_monitoring,
        device_sim_score=analysis_result.module_scores.device_sim,
        agent_fraud_score=analysis_result.module_scores.agent_fraud,
        fraud_graph_score=analysis_result.module_scores.fraud_graph,
        final_risk_score=analysis_result.risk_score,
        trust_score=analysis_result.trust_score,
        reasons_json=json.dumps(analysis_result.reasons, ensure_ascii=False),
        created_at=datetime.utcnow(),
    )
    db.add(risk_score)
    db.commit()
    db.refresh(risk_score)
    return risk_score


def get_risk_score_by_transaction_id(db: Session, transaction_id: str) -> RiskScore | None:
    return db.query(RiskScore).filter(RiskScore.transaction_id == transaction_id).first()
