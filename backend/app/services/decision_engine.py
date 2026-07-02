"""Decision logic for transaction outcomes."""

from app.core.constants import (
    DECISION_ALLOW,
    DECISION_MONITOR,
    DECISION_REVIEW,
    DECISION_TEMPORARY_BLOCK,
    RISK_LEVEL_CRITICAL,
    RISK_LEVEL_HIGH,
    RISK_LEVEL_LOW,
    RISK_LEVEL_MODERATE,
)


class DecisionEngine:
    """Map a risk score to a decision and a readable risk level."""

    def decide(self, risk_score: int) -> tuple[str, str]:
        if risk_score <= 29:
            return DECISION_ALLOW, RISK_LEVEL_LOW
        if risk_score <= 59:
            return DECISION_MONITOR, RISK_LEVEL_MODERATE
        if risk_score <= 79:
            return DECISION_REVIEW, RISK_LEVEL_HIGH
        return DECISION_TEMPORARY_BLOCK, RISK_LEVEL_CRITICAL

