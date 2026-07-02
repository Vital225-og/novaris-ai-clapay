"""Transaction ORM model."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=False)
    sender_phone = Column(String, nullable=True)
    receiver_phone = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    agent_id = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
    location = Column(String, nullable=True)
    hour = Column(Integer, nullable=True)
    transactions_last_10min = Column(Integer, nullable=True)
    is_new_device = Column(Boolean, nullable=False, default=False)
    sim_changed_recently = Column(Boolean, nullable=False, default=False)
    agent_risk_level = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=False)
    trust_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    investigation_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    alert_id = Column(String, nullable=True)
    alert_status = Column(String, nullable=True)

