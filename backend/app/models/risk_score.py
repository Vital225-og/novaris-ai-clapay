"""Risk score ORM model."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    transaction_monitoring_score = Column(Integer, nullable=False)
    device_sim_score = Column(Integer, nullable=False)
    agent_fraud_score = Column(Integer, nullable=False)
    fraud_graph_score = Column(Integer, nullable=False)
    final_risk_score = Column(Integer, nullable=False)
    trust_score = Column(Integer, nullable=False)
    reasons_json = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

