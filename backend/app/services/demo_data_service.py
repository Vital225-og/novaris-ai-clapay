"""Load structured demo data for the in-memory store."""

from __future__ import annotations

import json
from pathlib import Path

from app.schemas.alert_schema import AlertRecord
from app.schemas.transaction_schema import TransactionRecord


class DemoDataService:
    """Read demo transactions and alerts from JSON files."""

    def __init__(self) -> None:
        self.data_dir = Path(__file__).resolve().parents[1] / "data"

    def load_demo_transactions(self) -> list[TransactionRecord]:
        payload = self._read_json("demo_transactions.json")
        return [TransactionRecord.model_validate(item) for item in payload]

    def load_demo_alerts(self) -> list[AlertRecord]:
        payload = self._read_json("demo_alerts.json")
        return [AlertRecord.model_validate(item) for item in payload]

    def _read_json(self, filename: str) -> list[dict[str, object]]:
        file_path = self.data_dir / filename
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

