"""Coordinate scoring, decisioning and explanation generation."""

from app.core.exceptions import AnalysisError
from app.schemas.risk_schema import ModuleScores
from app.schemas.transaction_schema import TransactionAnalysisRequest, TransactionAnalysisResponse
from app.services.ai_investigator import AIInvestigator
from app.services.decision_engine import DecisionEngine
from app.services.trust_score_engine import TrustScoreEngine
from app.utils.id_generator import generate_transaction_id


class RiskOrchestrator:
    """Orchestrate the Sprint 1 risk analysis flow."""

    def __init__(
        self,
        trust_score_engine: TrustScoreEngine | None = None,
        decision_engine: DecisionEngine | None = None,
        ai_investigator: AIInvestigator | None = None,
    ) -> None:
        self.trust_score_engine = trust_score_engine or TrustScoreEngine()
        self.decision_engine = decision_engine or DecisionEngine()
        self.ai_investigator = ai_investigator or AIInvestigator()

    def analyze(self, transaction: TransactionAnalysisRequest) -> TransactionAnalysisResponse:
        try:
            risk_score = self._calculate_risk_score(transaction)
            trust_score = self.trust_score_engine.calculate(risk_score)
            decision, risk_level = self.decision_engine.decide(risk_score)
            module_scores = self._calculate_module_scores(transaction)
            reasons = self._build_reasons(transaction)
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

    def _calculate_risk_score(self, transaction: TransactionAnalysisRequest) -> int:
        score = 0
        if transaction.amount >= 300000:
            score += 35
        elif transaction.amount >= 100000:
            score += 20

        if transaction.transactions_last_10min >= 5:
            score += 20
        elif transaction.transactions_last_10min >= 3:
            score += 10

        if 0 <= transaction.hour <= 5:
            score += 8

        if transaction.is_new_device:
            score += 12

        if transaction.sim_changed_recently:
            score += 10

        if transaction.agent_risk_level == "high":
            score += 7
        elif transaction.agent_risk_level == "medium":
            score += 4

        return min(100, score)

    def _calculate_module_scores(self, transaction: TransactionAnalysisRequest) -> ModuleScores:
        transaction_monitoring = 0
        transaction_monitoring += 50 if transaction.amount >= 300000 else 20 if transaction.amount >= 100000 else 5
        transaction_monitoring += 25 if transaction.transactions_last_10min >= 5 else 10 if transaction.transactions_last_10min >= 3 else 0
        transaction_monitoring += 15 if 0 <= transaction.hour <= 5 else 0

        device_sim = 50 if transaction.is_new_device else 20
        device_sim += 35 if transaction.sim_changed_recently else 5

        agent_fraud = 75 if transaction.agent_risk_level == "high" else 45 if transaction.agent_risk_level == "medium" else 20

        fraud_graph = 55
        fraud_graph += 15 if transaction.amount >= 300000 else 5
        fraud_graph += 8 if transaction.transactions_last_10min >= 5 else 0
        fraud_graph += 5 if transaction.is_new_device else 0
        fraud_graph += 5 if transaction.agent_risk_level == "high" else 0

        return ModuleScores(
            transaction_monitoring=min(100, transaction_monitoring),
            device_sim=min(100, device_sim),
            agent_fraud=min(100, agent_fraud),
            fraud_graph=min(100, fraud_graph),
        )

    def _build_reasons(self, transaction: TransactionAnalysisRequest) -> list[str]:
        reasons: list[str] = []

        if transaction.amount >= 300000:
            reasons.append("Montant très supérieur au comportement habituel")
        if transaction.transactions_last_10min >= 5:
            reasons.append("Fréquence élevée sur une courte période")
        if transaction.is_new_device:
            reasons.append("Nouvel appareil détecté")
        if transaction.sim_changed_recently:
            reasons.append("SIM changée récemment")
        if transaction.agent_risk_level == "high":
            reasons.append("Agent associé à un niveau de risque élevé")

        return reasons or ["Aucun signal de fraude critique détecté"]
