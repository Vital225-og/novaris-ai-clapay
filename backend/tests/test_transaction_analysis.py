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
    assert body["risk_level"] == "Critique"
    assert body["risk_score"] == 82
    assert body["trust_score"] == 180
    assert body["trust_score"] == 1000 - body["risk_score"] * 10


def test_response_contains_expected_fields() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/transactions/analyze", json=_risk_payload())

    body = response.json()

    assert "risk_score" in body
    assert "trust_score" in body
    assert "decision" in body
    assert "reasons" in body
    assert "investigation_summary" in body
    assert "module_scores" in body
    assert isinstance(body["module_scores"], dict)
    assert set(body["module_scores"].keys()) == {
        "transaction_monitoring",
        "device_sim",
        "agent_fraud",
        "fraud_graph",
    }
    assert isinstance(body["reasons"], list)
    assert any("Montant" in reason for reason in body["reasons"])
    assert any("appareil" in reason.lower() for reason in body["reasons"])
    assert any("agent" in reason.lower() for reason in body["reasons"])
