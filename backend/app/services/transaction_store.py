"""SQLite-backed transaction access."""

from __future__ import annotations

from json import loads
from threading import Lock

from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.seed_demo_data import seed_demo_data
from app.repositories.risk_score_repository import create_risk_score, get_risk_score_by_transaction_id
from app.repositories.transaction_repository import (
    create_transaction,
    get_all_transactions,
    get_transaction_by_id,
)
from app.schemas.risk_schema import ModuleScores
from app.schemas.transaction_schema import (
    TransactionAnalysisRequest,
    TransactionAnalysisResponse,
    TransactionRecord,
)
from app.db.session import SessionLocal


class TransactionStore:
    """Persist and retrieve transactions via SQLite."""

    def __init__(self) -> None:
        self._lock = Lock()

    def reset(self, db: Session | None = None) -> None:
        if db is None:
            with SessionLocal() as session:
                self.reset(session)
            return

        with self._lock:
            init_db(drop_existing=True)
            seed_demo_data(db)

    def list_transactions(self, db: Session | None = None) -> list[TransactionRecord]:
        if db is None:
            with SessionLocal() as session:
                return self.list_transactions(session)

        transactions = get_all_transactions(db)
        return [self._to_record(transaction, db) for transaction in transactions]

    def get_transaction(self, transaction_id: str, db: Session | None = None) -> TransactionRecord | None:
        if db is None:
            with SessionLocal() as session:
                return self.get_transaction(transaction_id, session)

        transaction = get_transaction_by_id(db, transaction_id)
        if transaction is None:
            return None
        return self._to_record(transaction, db)

    def add_transaction(
        self,
        db: Session | None,
        payload: TransactionAnalysisRequest,
        analysis_result: TransactionAnalysisResponse,
    ) -> TransactionRecord:
        if db is None:
            with SessionLocal() as session:
                return self.add_transaction(session, payload, analysis_result)

        with self._lock:
            transaction = create_transaction(db, payload, analysis_result)
            create_risk_score(db, analysis_result)
            return self._to_record(transaction, db)

    def attach_alert(self, transaction_id: str, alert_id: str, alert_status: str, db: Session | None = None) -> None:
        if db is None:
            with SessionLocal() as session:
                self.attach_alert(transaction_id, alert_id, alert_status, session)
            return

        transaction = get_transaction_by_id(db, transaction_id)
        if transaction is None:
            return
        transaction.alert_id = alert_id
        transaction.alert_status = alert_status
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

    def _to_record(self, transaction, db: Session) -> TransactionRecord:
        risk_score = get_risk_score_by_transaction_id(db, transaction.transaction_id)
        module_scores = ModuleScores(
            transaction_monitoring=risk_score.transaction_monitoring_score if risk_score else 0,
            device_sim=risk_score.device_sim_score if risk_score else 0,
            agent_fraud=risk_score.agent_fraud_score if risk_score else 0,
            fraud_graph=risk_score.fraud_graph_score if risk_score else 0,
        )
        reasons = loads(risk_score.reasons_json) if risk_score else []

        return TransactionRecord(
            transaction_id=transaction.transaction_id,
            customer_name=transaction.customer_name,
            sender_phone=transaction.sender_phone,
            receiver_phone=transaction.receiver_phone,
            amount=int(transaction.amount),
            transaction_type=transaction.transaction_type,
            agent_id=transaction.agent_id,
            device_id=transaction.device_id,
            location=transaction.location,
            hour=transaction.hour,
            transactions_last_10min=transaction.transactions_last_10min,
            is_new_device=transaction.is_new_device,
            sim_changed_recently=transaction.sim_changed_recently,
            agent_risk_level=transaction.agent_risk_level,
            risk_score=transaction.risk_score,
            trust_score=transaction.trust_score,
            risk_level=transaction.risk_level,
            decision=transaction.decision,
            module_scores=module_scores,
            reasons=reasons,
            investigation_summary=transaction.investigation_summary,
            created_at=transaction.created_at.replace(microsecond=0).isoformat(),
            alert_id=transaction.alert_id,
            alert_status=transaction.alert_status,
        )


transaction_store = TransactionStore()
