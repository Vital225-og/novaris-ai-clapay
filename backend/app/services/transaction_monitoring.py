"""Transaction monitoring scoring service."""

from app.schemas.risk_schema import ScoreResult
from app.schemas.transaction_schema import TransactionAnalysisRequest


class TransactionMonitoringService:
    """Score transactional behavior using deterministic rules."""

    def analyze(self, transaction: TransactionAnalysisRequest) -> ScoreResult:
        score = 0
        reasons: list[str] = []

        if transaction.amount >= 300000:
            score += 35
            reasons.append("Montant très supérieur au comportement habituel")
        elif transaction.amount >= 100000:
            score += 20
            reasons.append("Montant supérieur au comportement habituel")

        if transaction.transactions_last_10min >= 8:
            score += 30
            reasons.append("Volume très élevé sur une courte période")
        elif transaction.transactions_last_10min >= 5:
            score += 20
            reasons.append("Fréquence élevée sur une courte période")

        if 0 <= transaction.hour <= 5:
            score += 15
            reasons.append("Transaction réalisée pendant une plage horaire sensible")

        if transaction.transaction_type.lower() == "withdrawal":
            score += 10
            reasons.append("Type de transaction à risque: retrait")

        return ScoreResult(score=min(100, score), reasons=reasons)

