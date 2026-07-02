"""Coordinate scoring, decisioning and explanation generation."""

from app.core.exceptions import AnalysisError
from app.schemas.risk_schema import ModuleScores
from app.schemas.transaction_schema import TransactionAnalysisRequest, TransactionAnalysisResponse
from app.services.ai_investigator import AIInvestigator
from app.services.agent_fraud_detection import AgentFraudDetectionService
from app.services.decision_engine import DecisionEngine
from app.services.device_sim_intelligence import DeviceSimIntelligenceService
from app.services.fraud_graph_service import FraudGraphService
from app.services.transaction_monitoring import TransactionMonitoringService
from app.services.trust_score_engine import TrustScoreEngine
from app.utils.id_generator import generate_transaction_id


class RiskOrchestrator:
    """Coordinate the modular risk scoring services."""

    def __init__(
        self,
        trust_score_engine: TrustScoreEngine | None = None,
        decision_engine: DecisionEngine | None = None,
        ai_investigator: AIInvestigator | None = None,
        transaction_monitoring_service: TransactionMonitoringService | None = None,
        device_sim_intelligence_service: DeviceSimIntelligenceService | None = None,
        agent_fraud_detection_service: AgentFraudDetectionService | None = None,
        fraud_graph_service: FraudGraphService | None = None,
    ) -> None:
        self.trust_score_engine = trust_score_engine or TrustScoreEngine()
        self.decision_engine = decision_engine or DecisionEngine()
        self.ai_investigator = ai_investigator or AIInvestigator()
        self.transaction_monitoring_service = transaction_monitoring_service or TransactionMonitoringService()
        self.device_sim_intelligence_service = device_sim_intelligence_service or DeviceSimIntelligenceService()
        self.agent_fraud_detection_service = agent_fraud_detection_service or AgentFraudDetectionService()
        self.fraud_graph_service = fraud_graph_service or FraudGraphService()

    def analyze(self, transaction: TransactionAnalysisRequest) -> TransactionAnalysisResponse:
        try:
            transaction_monitoring = self.transaction_monitoring_service.analyze(transaction)
            device_sim = self.device_sim_intelligence_service.analyze(transaction)
            agent_fraud = self.agent_fraud_detection_service.analyze(transaction)
            fraud_graph = self.fraud_graph_service.analyze(transaction)

            module_scores = ModuleScores(
                transaction_monitoring=transaction_monitoring.score,
                device_sim=device_sim.score,
                agent_fraud=agent_fraud.score,
                fraud_graph=fraud_graph.score,
            )
            reasons = self._aggregate_reasons(
                transaction_monitoring.reasons,
                device_sim.reasons,
                agent_fraud.reasons,
                fraud_graph.reasons,
            )
            risk_score = self._calculate_risk_score(module_scores)
            trust_score = self.trust_score_engine.calculate(risk_score)
            decision, risk_level = self.decision_engine.decide(risk_score)
            investigation_summary = self.ai_investigator.summarize(risk_level, decision, reasons)
        except Exception as exc:  # pragma: no cover - defensive guard
            raise AnalysisError("Unable to analyze transaction") from exc

        return TransactionAnalysisResponse(
            transaction_id=generate_transaction_id(),
            customer_name=transaction.customer_name,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
            agent_id=transaction.agent_id,
            device_id=transaction.device_id,
            location=transaction.location,
            risk_score=risk_score,
            trust_score=trust_score,
            risk_level=risk_level,
            decision=decision,
            module_scores=module_scores,
            reasons=reasons,
            investigation_summary=investigation_summary,
        )

    def _calculate_risk_score(self, module_scores: ModuleScores) -> int:
        weighted_score = (
            0.35 * module_scores.transaction_monitoring
            + 0.25 * module_scores.device_sim
            + 0.20 * module_scores.agent_fraud
            + 0.20 * module_scores.fraud_graph
        )
        return max(0, min(100, round(weighted_score)))

    def _aggregate_reasons(self, *reason_groups: list[str]) -> list[str]:
        aggregated: list[str] = []
        seen: set[str] = set()

        for group in reason_groups:
            for reason in group:
                if reason not in seen:
                    seen.add(reason)
                    aggregated.append(reason)

        return aggregated or ["Aucun signal de fraude critique détecté"]
