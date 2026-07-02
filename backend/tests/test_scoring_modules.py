from app.schemas.transaction_schema import TransactionAnalysisRequest
from app.services.agent_fraud_detection import AgentFraudDetectionService
from app.services.device_sim_intelligence import DeviceSimIntelligenceService
from app.services.fraud_graph_service import FraudGraphService
from app.services.risk_orchestrator import RiskOrchestrator
from app.services.transaction_monitoring import TransactionMonitoringService


def _payload() -> TransactionAnalysisRequest:
    return TransactionAnalysisRequest(
        customer_name="Client Demo",
        sender_phone="+2250700000000",
        receiver_phone="+2250500000000",
        amount=450000,
        transaction_type="withdrawal",
        agent_id="AG-044",
        device_id="DEV-NEW-991",
        location="Abidjan",
        hour=1,
        transactions_last_10min=8,
        is_new_device=True,
        sim_changed_recently=True,
        agent_risk_level="high",
    )


def test_transaction_monitoring_high_risk() -> None:
    result = TransactionMonitoringService().analyze(_payload())

    assert result.score == 90
    assert len(result.reasons) >= 3


def test_device_sim_high_risk() -> None:
    result = DeviceSimIntelligenceService().analyze(_payload())

    assert result.score == 75
    assert "Nouvel appareil détecté" in result.reasons
    assert "SIM changée récemment" in result.reasons


def test_agent_fraud_high_risk() -> None:
    result = AgentFraudDetectionService().analyze(_payload())

    assert result.score == 75
    assert "Agent associé à un niveau de risque élevé" in result.reasons


def test_fraud_graph_returns_score() -> None:
    result = FraudGraphService().analyze(_payload())

    assert result.score == 85
    assert len(result.reasons) >= 3


def test_orchestrator_aggregates_module_scores() -> None:
    result = RiskOrchestrator().analyze(_payload())

    assert result.module_scores.transaction_monitoring == 90
    assert result.module_scores.device_sim == 75
    assert result.module_scores.agent_fraud == 75
    assert result.module_scores.fraud_graph == 85
    assert result.risk_score == 82
    assert result.trust_score == 180
    assert result.decision == "TEMPORARY_BLOCK"
    assert result.risk_level == "Critique"
    assert len(result.reasons) >= 4
