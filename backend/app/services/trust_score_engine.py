"""Deterministic trust score calculations for Sprint 1."""


class TrustScoreEngine:
    """Convert a risk score into a Novaris Trust Score."""

    def calculate(self, risk_score: int) -> int:
        trust_score = 1000 - (risk_score * 10)
        return max(0, min(1000, trust_score))

