"""Dashboard KPI calculations."""

from __future__ import annotations

from statistics import mean

from app.schemas.dashboard_schema import DashboardKPIResponse
from app.services.alert_service import alert_service
from app.services.transaction_store import transaction_store


class DashboardService:
    """Aggregate in-memory metrics for the dashboard."""

    def get_kpis(self) -> DashboardKPIResponse:
        transactions = transaction_store.list_transactions()
        alerts = alert_service.list_alerts()

        total_transactions = len(transactions)
        total_alerts = len(alerts)
        critical_alerts = sum(1 for alert in alerts if alert.risk_level == "Critique")
        review_alerts = sum(1 for alert in alerts if alert.risk_level == "Élevé")
        allowed_transactions = sum(1 for tx in transactions if tx.decision == "ALLOW")
        blocked_transactions = sum(1 for tx in transactions if tx.decision == "TEMPORARY_BLOCK")
        protected_amount = sum(
            tx.amount for tx in transactions if tx.decision == "TEMPORARY_BLOCK"
        )
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

