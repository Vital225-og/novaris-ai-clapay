from fastapi.testclient import TestClient

from app.main import app


def _risk_payload() -> dict[str, object]:
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


def test_transaction_analysis_returns_200() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/transactions/analyze", json=_risk_payload())

    assert response.status_code == 200


def test_very_risky_transaction_returns_temporary_block() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/transactions/analyze", json=_risk_payload())

    body = response.json()

    assert body["decision"] == "TEMPORARY_BLOCK"
    assert body["risk_score"] == 92
    assert body["trust_score"] == 80


def test_response_contains_expected_fields() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/transactions/analyze", json=_risk_payload())

    body = response.json()

    assert "risk_score" in body
    assert "trust_score" in body
    assert "decision" in body
    assert "reasons" in body
    assert "investigation_summary" in body
    assert isinstance(body["reasons"], list)
    assert len(body["reasons"]) > 0
