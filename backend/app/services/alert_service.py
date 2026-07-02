"""SQLite-backed alert management service."""

from __future__ import annotations

from datetime import datetime
from threading import Lock

from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.seed_demo_data import seed_demo_data
from app.db.session import SessionLocal
from app.repositories.alert_repository import (
    create_alert,
    get_alert_by_id,
    get_all_alerts,
    resolve_alert as resolve_alert_record,
)
from app.repositories.transaction_repository import update_transaction_alert
from app.schemas.alert_schema import AlertRecord
from app.schemas.transaction_schema import TransactionAnalysisResponse, TransactionRecord


class AlertService:
    """Manage fraud alerts in SQLite."""

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

    def list_alerts(self, db: Session | None = None) -> list[AlertRecord]:
        if db is None:
            with SessionLocal() as session:
                return self.list_alerts(session)

        return [self._to_record(alert) for alert in get_all_alerts(db)]

    def get_alert(self, alert_id: str, db: Session | None = None) -> AlertRecord | None:
        if db is None:
            with SessionLocal() as session:
                return self.get_alert(alert_id, session)

        alert = get_alert_by_id(db, alert_id)
        return self._to_record(alert) if alert is not None else None

    def create_alert_from_transaction(
        self,
        db: Session | None,
        transaction: TransactionAnalysisResponse | TransactionRecord,
    ) -> AlertRecord | None:
        if transaction.risk_score < 60:
            return None

        if db is None:
            with SessionLocal() as session:
                return self.create_alert_from_transaction(session, transaction)

        with self._lock:
            alert = create_alert(db, transaction)
            update_transaction_alert(db, transaction.transaction_id, alert.alert_id, alert.status)
            return self._to_record(alert)

    def resolve_alert(self, alert_id: str, db: Session | None = None) -> AlertRecord | None:
        if db is None:
            with SessionLocal() as session:
                return self.resolve_alert(alert_id, session)

        with self._lock:
            alert = resolve_alert_record(db, alert_id)
            if alert is None:
                return None
            update_transaction_alert(db, alert.transaction_id, alert.alert_id, alert.status)
            return self._to_record(alert)

    def _to_record(self, alert) -> AlertRecord:
        return AlertRecord(
            alert_id=alert.alert_id,
            transaction_id=alert.transaction_id,
            risk_score=alert.risk_score,
            risk_level=alert.risk_level,
            decision=alert.decision,
            status=alert.status,
            created_at=alert.created_at.replace(microsecond=0).isoformat(),
            main_reason=alert.main_reason or "",
            resolved_at=alert.resolved_at.replace(microsecond=0).isoformat() if alert.resolved_at else None,
        )


alert_service = AlertService()
