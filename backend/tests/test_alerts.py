from fastapi.testclient import TestClient

from app.main import app
from app.services.alert_service import alert_service
from app.services.transaction_store import transaction_store


def _client() -> TestClient:
    return TestClient(app)


def setup_function() -> None:
    transaction_store.reset()
    alert_service.reset()


def test_get_alerts_returns_200() -> None:
    with _client() as client:
        response = client.get("/api/v1/alerts")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_critical_transaction_creates_alert() -> None:
    payload = {
        "customer_name": "Client Demo",
        "sender_phone": "+2250700000000",
        "receiver_phone": "+2250500000000",
        "amount": 450000,
        "transaction_type": "withdrawal",
        "agent_id": "AG-044",
        "device_id": "DEV-NEW-991",
        "location": "Abidjan",
        "hour": 1,
        "transactions_last_10min": 8,
        "is_new_device": True,
        "sim_changed_recently": True,
        "agent_risk_level": "high",
    }

    with _client() as client:
        analysis = client.post("/api/v1/transactions/analyze", json=payload)
        assert analysis.status_code == 200
        alerts = client.get("/api/v1/alerts")

    alert_items = alerts.json()
    created_alert = next(item for item in alert_items if item["transaction_id"] == analysis.json()["transaction_id"])

    assert created_alert["status"] == "OPEN"
    assert created_alert["risk_level"] == "Critique"
    assert created_alert["decision"] == "TEMPORARY_BLOCK"


def test_resolve_alert_changes_status_to_resolved() -> None:
    with _client() as client:
        response = client.post("/api/v1/alerts/ALT-001/resolve")

    assert response.status_code == 200
    assert response.json()["status"] == "RESOLVED"
