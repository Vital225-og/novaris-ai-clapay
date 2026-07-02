"""Agent fraud detection scoring service."""

from app.schemas.risk_schema import ScoreResult
from app.schemas.transaction_schema import TransactionAnalysisRequest


class AgentFraudDetectionService:
    """Score agent risk using deterministic rules."""

    def analyze(self, transaction: TransactionAnalysisRequest) -> ScoreResult:
        score = 0
        reasons: list[str] = []

        if not transaction.agent_id.strip():
            score += 10
            reasons.append("Identifiant agent manquant")

        if transaction.agent_risk_level == "high":
            score += 75
            reasons.append("Agent associé à un niveau de risque élevé")
        elif transaction.agent_risk_level == "medium":
            score += 45
            reasons.append("Agent associé à un niveau de risque modéré")
        else:
            score += 15
            reasons.append("Agent associé à un niveau de risque faible")

        return ScoreResult(score=min(100, score), reasons=reasons)

