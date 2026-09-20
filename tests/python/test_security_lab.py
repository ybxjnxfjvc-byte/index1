from __future__ import annotations

import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "lab"
sys.path.insert(0, str(LAB))

from mock_api import validate_payload  # noqa: E402
from sqlite_store import connect, insert_result, get_result  # noqa: E402


def valid_payload():
    return {
        "trainerId": "sber-cross-sales-v1",
        "participant": "O'Reilly <img src=x onerror=alert(1)>",
        "unit": "demo'; DROP TABLE training_results; --",
        "score": 8,
        "total": 10,
        "completedAt": "2026-09-19T12:00:00.000Z",
        "answers": [],
    }


class ValidationTests(unittest.TestCase):
    def test_valid_payload_is_accepted(self):
        ok, reason = validate_payload(valid_payload())
        self.assertTrue(ok, reason)

    def test_unknown_field_is_rejected(self):
        p = valid_payload()
        p["password"] = "not-allowed"
        ok, reason = validate_payload(p)
        self.assertFalse(ok)
        self.assertEqual(reason, "unknown-field")

    def test_score_cannot_exceed_total(self):
        p = valid_payload()
        p["score"] = 11
        ok, reason = validate_payload(p)
        self.assertFalse(ok)
        self.assertEqual(reason, "score-exceeds-total")

    def test_overlong_participant_is_rejected(self):
        p = valid_payload()
        p["participant"] = "A" * 81
        ok, _ = validate_payload(p)
        self.assertFalse(ok)


class SqliteTests(unittest.TestCase):
    def test_parameterized_insert_preserves_sql_like_text(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "test.db"
            conn = connect(db)
            try:
                payload = valid_payload()
                row_id = insert_result(conn, payload)
                stored = get_result(conn, row_id)
                self.assertEqual(stored["participant"], payload["participant"])
                self.assertEqual(stored["unit"], payload["unit"])
                # Table must still exist after SQL-looking text.
                count = conn.execute("SELECT COUNT(*) FROM training_results").fetchone()[0]
                self.assertEqual(count, 1)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
