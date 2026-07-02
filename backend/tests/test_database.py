from sqlalchemy import inspect

from app.db.database import engine
from app.db.init_db import init_db


def test_database_is_initialized() -> None:
    init_db(drop_existing=True)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    assert {"transactions", "alerts", "risk_scores"}.issubset(tables)

