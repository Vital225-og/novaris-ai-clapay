"""Alert repository."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.transaction_schema import TransactionAnalysisResponse, TransactionRecord
from app.utils.id_generator import generate_alert_id


def create_alert(db: Session, analysis_result: TransactionAnalysisResponse | TransactionRecord) -> Alert:
    alert = Alert(
        alert_id=generate_alert_id(),
        transaction_id=analysis_result.transaction_id,
        risk_score=analysis_result.risk_score,
        risk_level="Critique" if analysis_result.risk_score >= 80 else "Élevé",
        decision="TEMPORARY_BLOCK" if analysis_result.risk_score >= 80 else "REVIEW",
        status="OPEN" if analysis_result.risk_score >= 80 else "IN_REVIEW",
        main_reason=_compose_main_reason(analysis_result.reasons),
        created_at=datetime.utcnow(),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_all_alerts(db: Session) -> list[Alert]:
    return db.query(Alert).order_by(Alert.created_at.asc(), Alert.id.asc()).all()


def get_alert_by_id(db: Session, alert_id: str) -> Alert | None:
    return db.query(Alert).filter(Alert.alert_id == alert_id).first()


def resolve_alert(db: Session, alert_id: str) -> Alert | None:
    alert = get_alert_by_id(db, alert_id)
    if alert is None:
        return None
    alert.status = "RESOLVED"
    alert.resolved_at = datetime.utcnow()
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def _compose_main_reason(reasons: list[str]) -> str:
    if not reasons:
        return "Signal de risque détecté"
    return " + ".join(reasons[:2])
