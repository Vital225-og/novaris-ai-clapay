"""Custom application exceptions."""


class NovarisError(Exception):
    """Base exception for Novaris backend errors."""


class AnalysisError(NovarisError):
    """Raised when an analysis request cannot be processed."""

