"""In-memory transaction storage."""

from __future__ import annotations

from threading import Lock

from app.schemas.transaction_schema import TransactionAnalysisResponse, TransactionRecord
from app.services.demo_data_service import DemoDataService


class TransactionStore:
    """Store demo and analyzed transactions in memory."""

    def __init__(self, demo_data_service: DemoDataService | None = None) -> None:
        self.demo_data_service = demo_data_service or DemoDataService()
        self._lock = Lock()
        self._transactions: list[TransactionRecord] = []
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._transactions = self.demo_data_service.load_demo_transactions()

    def list_transactions(self) -> list[TransactionRecord]:
        with self._lock:
            return list(self._transactions)

    def get_transaction(self, transaction_id: str) -> TransactionRecord | None:
        with self._lock:
            for transaction in self._transactions:
                if transaction.transaction_id == transaction_id:
                    return transaction
        return None

    def add_transaction(self, transaction: TransactionAnalysisResponse) -> TransactionRecord:
        record = TransactionRecord(
            **transaction.model_dump(),
            created_at=self._current_timestamp(),
            alert_id=None,
            alert_status=None,
        )
        with self._lock:
            self._transactions.append(record)
        return record

    def attach_alert(self, transaction_id: str, alert_id: str, alert_status: str) -> None:
        with self._lock:
            for index, transaction in enumerate(self._transactions):
                if transaction.transaction_id == transaction_id:
                    self._transactions[index] = transaction.model_copy(
                        update={"alert_id": alert_id, "alert_status": alert_status}
                    )
                    break

    def _current_timestamp(self) -> str:
        from datetime import datetime

        return datetime.utcnow().replace(microsecond=0).isoformat()


transaction_store = TransactionStore()

