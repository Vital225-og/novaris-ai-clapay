"""Identifiers helpers."""

from uuid import uuid4


def generate_transaction_id() -> str:
    """Generate a human-friendly transaction identifier."""
    return f"TX-{uuid4().hex[:12].upper()}"


def generate_alert_id() -> str:
    """Generate a human-friendly alert identifier."""
    return f"ALT-{uuid4().hex[:6].upper()}"
