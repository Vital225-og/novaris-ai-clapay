"""Identifiers helpers."""

from uuid import uuid4


def generate_transaction_id() -> str:
    """Generate a human-friendly transaction identifier."""
    return f"TX-{uuid4().hex[:12].upper()}"

