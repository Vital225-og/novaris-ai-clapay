"""Database session helpers."""

from sqlalchemy.orm import sessionmaker

from app.db.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

