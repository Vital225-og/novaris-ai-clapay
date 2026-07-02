"""Pytest configuration for isolated SQLite tests."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


TEST_DB_PATH = Path(tempfile.gettempdir()).joinpath("novaris_ai_test.db").resolve()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"

if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()

from app.db.database import engine


def pytest_sessionfinish(session, exitstatus):  # noqa: D401, ANN001
    engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
