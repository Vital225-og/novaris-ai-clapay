"""Transaction repository."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionAnalysisRequest, TransactionAnalysisResponse


def create_transaction(db: Session, payload: TransactionAnalysisRequest, analysis_result: TransactionAnalysisResponse) -> Transaction:
    transaction = Transaction(
        transaction_id=analysis_result.transaction_id,
        customer_name=analysis_result.customer_name,
        sender_phone=payload.sender_phone,
        receiver_phone=payload.receiver_phone,
        amount=float(analysis_result.amount),
        transaction_type=analysis_result.transaction_type,
        agent_id=analysis_result.agent_id,
        device_id=analysis_result.device_id,
        location=analysis_result.location,
        hour=payload.hour,
        transactions_last_10min=payload.transactions_last_10min,
        is_new_device=payload.is_new_device,
        sim_changed_recently=payload.sim_changed_recently,
        agent_risk_level=payload.agent_risk_level,
        risk_score=analysis_result.risk_score,
        trust_score=analysis_result.trust_score,
        risk_level=analysis_result.risk_level,
        decision=analysis_result.decision,
        investigation_summary=analysis_result.investigation_summary,
        created_at=datetime.utcnow(),
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_all_transactions(db: Session) -> list[Transaction]:
    return db.query(Transaction).order_by(Transaction.created_at.asc(), Transaction.id.asc()).all()


def get_transaction_by_id(db: Session, transaction_id: str) -> Transaction | None:
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()


def update_transaction_alert(db: Session, transaction_id: str, alert_id: str, alert_status: str) -> Transaction | None:
    transaction = get_transaction_by_id(db, transaction_id)
    if transaction is None:
        return None
    transaction.alert_id = alert_id
    transaction.alert_status = alert_status
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

