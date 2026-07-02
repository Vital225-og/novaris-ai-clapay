"""Seed demo data into SQLite."""

from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.models.alert import Alert
from app.models.risk_score import RiskScore
from app.models.transaction import Transaction
from app.services.demo_data_service import DemoDataService


def seed_demo_data(db: Session) -> None:
    init_db()
    demo_data_service = DemoDataService()

    for record in demo_data_service.load_demo_transactions():
        existing = db.query(Transaction).filter(Transaction.transaction_id == record.transaction_id).first()
        if existing is None:
            transaction = Transaction(
                transaction_id=record.transaction_id,
                customer_name=record.customer_name,
                sender_phone=getattr(record, "sender_phone", None),
                receiver_phone=getattr(record, "receiver_phone", None),
                amount=record.amount,
                transaction_type=record.transaction_type,
                agent_id=record.agent_id,
                device_id=record.device_id,
                location=record.location,
                hour=getattr(record, "hour", None),
                transactions_last_10min=getattr(record, "transactions_last_10min", None),
                is_new_device=bool(getattr(record, "is_new_device", False)),
                sim_changed_recently=bool(getattr(record, "sim_changed_recently", False)),
                agent_risk_level=getattr(record, "agent_risk_level", None),
                risk_score=record.risk_score,
                trust_score=record.trust_score,
                risk_level=record.risk_level,
                decision=record.decision,
                investigation_summary=record.investigation_summary,
                created_at=_parse_datetime(getattr(record, "created_at", None)),
                alert_id=getattr(record, "alert_id", None),
                alert_status=getattr(record, "alert_status", None),
            )
            db.add(transaction)

        existing_score = db.query(RiskScore).filter(RiskScore.transaction_id == record.transaction_id).first()
        if existing_score is None:
            risk_score = RiskScore(
                transaction_id=record.transaction_id,
                transaction_monitoring_score=record.module_scores.transaction_monitoring,
                device_sim_score=record.module_scores.device_sim,
                agent_fraud_score=record.module_scores.agent_fraud,
                fraud_graph_score=record.module_scores.fraud_graph,
                final_risk_score=record.risk_score,
                trust_score=record.trust_score,
                reasons_json=json.dumps(record.reasons, ensure_ascii=False),
                created_at=_parse_datetime(getattr(record, "created_at", None)),
            )
            db.add(risk_score)

    for record in demo_data_service.load_demo_alerts():
        existing = db.query(Alert).filter(Alert.alert_id == record.alert_id).first()
        if existing is None:
            alert = Alert(
                alert_id=record.alert_id,
                transaction_id=record.transaction_id,
                risk_score=record.risk_score,
                risk_level=record.risk_level,
                decision=record.decision,
                status=record.status,
                main_reason=record.main_reason,
                created_at=_parse_datetime(getattr(record, "created_at", None)),
                resolved_at=_parse_optional_datetime(getattr(record, "resolved_at", None)),
            )
            db.add(alert)

    db.commit()


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()
    return datetime.fromisoformat(value)


def _parse_optional_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)
