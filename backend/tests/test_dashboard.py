from fastapi.testclient import TestClient

from app.main import app
from app.services.alert_service import alert_service
from app.services.transaction_store import transaction_store


def _client() -> TestClient:
    return TestClient(app)


def setup_function() -> None:
    transaction_store.reset()
    alert_service.reset()


def test_dashboard_kpis_returns_200() -> None:
    with _client() as client:
        response = client.get("/api/v1/dashboard/kpis")

    assert response.status_code == 200
    body = response.json()
    assert "total_transactions" in body
    assert "total_alerts" in body
    assert "average_risk_score" in body


def test_transactions_list_returns_list() -> None:
    with _client() as client:
        response = client.get("/api/v1/transactions")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 25


def test_transaction_detail_returns_200() -> None:
    with _client() as client:
        response = client.get("/api/v1/transactions/TX-001")

    assert response.status_code == 200
    body = response.json()
    assert body["transaction_id"] == "TX-001"
    assert "risk_score" in body

