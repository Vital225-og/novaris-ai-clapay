"""Schemas for transaction analysis input and output."""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.risk_schema import ModuleScores


class TransactionAnalysisRequest(BaseModel):
    customer_name: str = Field(min_length=1)
    sender_phone: str = Field(min_length=1)
    receiver_phone: str = Field(min_length=1)
    amount: int = Field(ge=0)
    transaction_type: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    device_id: str = Field(min_length=1)
    location: str = Field(min_length=1)
    hour: int = Field(ge=0, le=23)
    transactions_last_10min: int = Field(ge=0)
    is_new_device: bool
    sim_changed_recently: bool
    agent_risk_level: Literal["low", "medium", "high"]


class TransactionAnalysisResponse(BaseModel):
    transaction_id: str
    customer_name: str
    amount: int
    transaction_type: str
    agent_id: str
    device_id: str
    location: str
    risk_score: int
    trust_score: int
    risk_level: str
    decision: str
    module_scores: ModuleScores
    reasons: list[str]
    investigation_summary: str


class TransactionRecord(TransactionAnalysisResponse):
    sender_phone: str | None = None
    receiver_phone: str | None = None
    hour: int | None = None
    transactions_last_10min: int | None = None
    is_new_device: bool | None = None
    sim_changed_recently: bool | None = None
    agent_risk_level: str | None = None
    created_at: str
    alert_id: str | None = None
    alert_status: str | None = None
