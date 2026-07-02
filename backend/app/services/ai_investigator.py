"""Readable explanations for risk outcomes."""


class AIInvestigator:
    """Return a deterministic investigation summary for Sprint 1."""

    def summarize(self, risk_level: str, decision: str, reasons: list[str]) -> str:
        if decision == "TEMPORARY_BLOCK":
            return (
                "Cette transaction présente un risque critique. "
                "Un blocage temporaire est recommandé avant validation humaine."
            )
        if decision == "REVIEW":
            return (
                "Cette transaction requiert une revue manuelle en raison de signaux "
                f"de risque: {', '.join(reasons[:3])}."
            )
        if decision == "MONITOR":
            return (
                "Cette transaction doit être surveillée. Les signaux de risque restent "
                "modérés mais méritent un suivi."
            )
        return (
            f"Le profil de risque est {risk_level.lower()}. "
            "La transaction peut être autorisée selon les règles actuelles."
        )

