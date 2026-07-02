"""Database initialization helpers."""

from app.db.database import Base, engine
from app.models import alert, risk_score, transaction  # noqa: F401


def init_db(drop_existing: bool = False) -> None:
    if drop_existing:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

