"""Device and SIM intelligence scoring service."""

from app.schemas.risk_schema import ScoreResult
from app.schemas.transaction_schema import TransactionAnalysisRequest


class DeviceSimIntelligenceService:
    """Score device and SIM signals deterministically."""

    def analyze(self, transaction: TransactionAnalysisRequest) -> ScoreResult:
        score = 0
        reasons: list[str] = []

        if transaction.is_new_device:
            score += 35
            reasons.append("Nouvel appareil détecté")

        if transaction.sim_changed_recently:
            score += 40
            reasons.append("SIM changée récemment")

        if not transaction.location or transaction.location.strip().lower() in {"unknown", "inconnue", "inconnu"}:
            score += 10
            reasons.append("Localisation vide ou inconnue")

        if transaction.device_id and any(token in transaction.device_id.upper() for token in ("NEW", "RISK")):
            reasons.append("Identifiant appareil compatible avec un contexte sensible")

        return ScoreResult(score=min(100, score), reasons=reasons)

