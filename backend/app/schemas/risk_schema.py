"""Schemas for risk output data."""

from pydantic import BaseModel, Field


class ModuleScores(BaseModel):
    transaction_monitoring: int = Field(ge=0, le=100)
    device_sim: int = Field(ge=0, le=100)
    agent_fraud: int = Field(ge=0, le=100)
    fraud_graph: int = Field(ge=0, le=100)


class RiskAnalysis(BaseModel):
    risk_score: int = Field(ge=0, le=100)
    trust_score: int = Field(ge=0, le=1000)
    risk_level: str
    decision: str
    module_scores: ModuleScores
    reasons: list[str]
    investigation_summary: str

