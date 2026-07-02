"""Simulated fraud graph intelligence service."""

from app.schemas.risk_schema import ScoreResult
from app.schemas.transaction_schema import TransactionAnalysisRequest


class FraudGraphService:
    """Simulate graph-based fraud signals for Sprint 2."""

    def analyze(self, transaction: TransactionAnalysisRequest) -> ScoreResult:
        score = 0
        reasons: list[str] = []

        if transaction.device_id and any(token in transaction.device_id.upper() for token in ("NEW", "RISK")):
            score += 35
            reasons.append("Appareil relié à un nœud sensible du graphe")

        if transaction.receiver_phone.strip():
            score += 10
            reasons.append("Bénéficiaire présent dans le flux transactionnel")

        if transaction.agent_id.strip() and transaction.agent_risk_level == "high":
            score += 40
            reasons.append("Agent à haut risque connecté au graphe")

        if transaction.sender_phone.strip() == transaction.receiver_phone.strip():
            score += 15
            reasons.append("Expéditeur et bénéficiaire identiques dans le graphe")

        return ScoreResult(score=min(100, score), reasons=reasons)

