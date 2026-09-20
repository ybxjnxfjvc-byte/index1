"""Local educational SQLite store. No production or third-party data."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Mapping, Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS training_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trainer_id TEXT NOT NULL,
    participant TEXT NOT NULL,
    unit TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    completed_at TEXT NOT NULL,
    answer_count INTEGER NOT NULL
)
"""


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def insert_result(conn: sqlite3.Connection, payload: Mapping[str, Any]) -> int:
    """Insert with placeholders only; never concatenate untrusted values into SQL."""
    cur = conn.execute(
        """
        INSERT INTO training_results
        (trainer_id, participant, unit, score, total, completed_at, answer_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["trainerId"],
            payload["participant"],
            payload["unit"],
            payload["score"],
            payload["total"],
            payload["completedAt"],
            len(payload.get("answers", [])),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_result(conn: sqlite3.Connection, row_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT id, trainer_id, participant, unit, score, total, completed_at, answer_count
        FROM training_results WHERE id = ?
        """,
        (row_id,),
    ).fetchone()
    if row is None:
        return None
    keys = ["id", "trainerId", "participant", "unit", "score", "total", "completedAt", "answerCount"]
    return dict(zip(keys, row))
