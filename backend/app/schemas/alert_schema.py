"""Alert schemas."""

from typing import Literal

from pydantic import BaseModel, Field


AlertStatus = Literal["OPEN", "IN_REVIEW", "RESOLVED"]


class AlertRecord(BaseModel):
    alert_id: str
    transaction_id: str
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
    decision: str
    status: AlertStatus
    created_at: str
    main_reason: str


class AlertResolveResponse(AlertRecord):
    pass

