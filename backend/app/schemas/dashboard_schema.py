"""Dashboard schemas."""

from pydantic import BaseModel, Field


class DashboardKPIResponse(BaseModel):
    total_transactions: int = Field(ge=0)
    total_alerts: int = Field(ge=0)
    critical_alerts: int = Field(ge=0)
    review_alerts: int = Field(ge=0)
    allowed_transactions: int = Field(ge=0)
    blocked_transactions: int = Field(ge=0)
    protected_amount: int = Field(ge=0)
    average_risk_score: int = Field(ge=0, le=100)

