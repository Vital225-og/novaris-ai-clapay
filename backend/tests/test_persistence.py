from fastapi.testclient import TestClient

from app.db.database import engine
from app.db.session import SessionLocal
from app.main import app
from app.repositories.alert_repository import get_alert_by_id
from app.repositories.risk_score_repository import get_risk_score_by_transaction_id
from app.repositories.transaction_repository import get_transaction_by_id
from app.services.alert_service import alert_service
from app.services.transaction_store import transaction_store


def setup_function() -> None:
    transaction_store.reset()
    alert_service.reset()


def _critical_payload() -> dict[str, object]:
    return {
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


def test_transaction_alert_and_risk_score_are_persisted() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/transactions/analyze", json=_critical_payload())

    body = response.json()
    transaction_id = body["transaction_id"]

    with SessionLocal() as db:
        transaction = get_transaction_by_id(db, transaction_id)
        risk_score = get_risk_score_by_transaction_id(db, transaction_id)
        alert = get_alert_by_id(db, transaction.alert_id)

    assert transaction is not None
    assert risk_score is not None
    assert alert is not None
    assert transaction.risk_score == 82
    assert risk_score.final_risk_score == 82
    assert alert.status == "OPEN"


def test_resolving_alert_updates_database() -> None:
    with TestClient(app) as client:
        analysis = client.post("/api/v1/transactions/analyze", json=_critical_payload()).json()
        alert_id = client.get("/api/v1/alerts").json()[-1]["alert_id"]
        resolve = client.post(f"/api/v1/alerts/{alert_id}/resolve")

    assert resolve.status_code == 200
    assert resolve.json()["status"] == "RESOLVED"

    with SessionLocal() as db:
        alert = get_alert_by_id(db, alert_id)
        transaction = get_transaction_by_id(db, analysis["transaction_id"])

    assert alert is not None
    assert alert.status == "RESOLVED"
    assert transaction is not None
    assert transaction.alert_status == "RESOLVED"


def test_dashboard_reads_from_database() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/dashboard/kpis")

    body = response.json()

    assert response.status_code == 200
    assert body["total_transactions"] >= 25
    assert body["total_alerts"] >= 8
    assert body["average_risk_score"] >= 0

