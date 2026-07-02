"""Dashboard KPI calculations from SQLite."""

from __future__ import annotations

from statistics import mean

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.alert_repository import get_all_alerts
from app.repositories.transaction_repository import get_all_transactions
from app.schemas.dashboard_schema import DashboardKPIResponse


class DashboardService:
    """Aggregate KPI metrics from the database."""

    def get_kpis(self, db: Session | None = None) -> DashboardKPIResponse:
        if db is None:
            with SessionLocal() as session:
                return self.get_kpis(session)

        transactions = get_all_transactions(db)
        alerts = get_all_alerts(db)

        total_transactions = len(transactions)
        total_alerts = len(alerts)
        critical_alerts = sum(1 for alert in alerts if alert.risk_level == "Critique")
        review_alerts = sum(1 for alert in alerts if alert.risk_level == "Élevé")
        allowed_transactions = sum(1 for tx in transactions if tx.decision == "ALLOW")
        blocked_transactions = sum(1 for tx in transactions if tx.decision == "TEMPORARY_BLOCK")
        protected_amount = sum(tx.amount for tx in transactions if tx.decision == "TEMPORARY_BLOCK")
        average_risk_score = round(mean(tx.risk_score for tx in transactions)) if transactions else 0

        return DashboardKPIResponse(
            total_transactions=total_transactions,
            total_alerts=total_alerts,
            critical_alerts=critical_alerts,
            review_alerts=review_alerts,
            allowed_transactions=allowed_transactions,
            blocked_transactions=blocked_transactions,
            protected_amount=protected_amount,
            average_risk_score=average_risk_score,
        )


dashboard_service = DashboardService()

