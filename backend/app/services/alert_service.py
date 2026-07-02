"""Alert management service."""

from __future__ import annotations

from datetime import datetime
from threading import Lock

from app.schemas.alert_schema import AlertRecord
from app.schemas.transaction_schema import TransactionAnalysisResponse, TransactionRecord
from app.services.demo_data_service import DemoDataService
from app.services.transaction_store import transaction_store
from app.utils.id_generator import generate_alert_id


class AlertService:
    """Manage fraud alerts in memory."""

    def __init__(self, demo_data_service: DemoDataService | None = None) -> None:
        self.demo_data_service = demo_data_service or DemoDataService()
        self._lock = Lock()
        self._alerts: list[AlertRecord] = []
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._alerts = self.demo_data_service.load_demo_alerts()

    def list_alerts(self) -> list[AlertRecord]:
        with self._lock:
            return list(self._alerts)

    def get_alert(self, alert_id: str) -> AlertRecord | None:
        with self._lock:
            for alert in self._alerts:
                if alert.alert_id == alert_id:
                    return alert
        return None

    def create_alert_from_transaction(self, transaction: TransactionAnalysisResponse | TransactionRecord) -> AlertRecord | None:
        if transaction.risk_score < 60:
            return None

        status = "OPEN" if transaction.risk_score >= 80 else "IN_REVIEW"
        alert = AlertRecord(
            alert_id=generate_alert_id(),
            transaction_id=transaction.transaction_id,
            risk_score=transaction.risk_score,
            risk_level="Critique" if transaction.risk_score >= 80 else "Élevé",
            decision="TEMPORARY_BLOCK" if transaction.risk_score >= 80 else "REVIEW",
            status=status,
            created_at=datetime.utcnow().replace(microsecond=0).isoformat(),
            main_reason=self._compose_main_reason(transaction.reasons),
        )

        with self._lock:
            self._alerts.append(alert)

        transaction_store.attach_alert(transaction.transaction_id, alert.alert_id, alert.status)
        return alert

    def resolve_alert(self, alert_id: str) -> AlertRecord | None:
        with self._lock:
            for index, alert in enumerate(self._alerts):
                if alert.alert_id == alert_id:
                    resolved = alert.model_copy(update={"status": "RESOLVED"})
                    self._alerts[index] = resolved
                    transaction_store.attach_alert(resolved.transaction_id, resolved.alert_id, resolved.status)
                    return resolved
        return None

    def _compose_main_reason(self, reasons: list[str]) -> str:
        if not reasons:
            return "Signal de risque détecté"
        return " + ".join(reasons[:2])


alert_service = AlertService()

