"""Local-only authenticated training-results API for security practice.

Binds to 127.0.0.1 and is not intended for internet exposure.
"""
from __future__ import annotations

import hmac
import json
import os
import sys
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from sqlite_store import connect, insert_result

HOST = "127.0.0.1"
MAX_BODY = 4096
ALLOWED_FIELDS = {"trainerId", "participant", "unit", "score", "total", "completedAt", "answers"}
REQUIRED_FIELDS = {"trainerId", "participant", "unit", "score", "total", "completedAt"}


def validate_payload(data: Any) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "body-must-be-object"
    keys = set(data)
    if not REQUIRED_FIELDS.issubset(keys):
        return False, "missing-required-field"
    if not keys.issubset(ALLOWED_FIELDS):
        return False, "unknown-field"
    checks = [
        isinstance(data["trainerId"], str) and 1 <= len(data["trainerId"]) <= 80,
        isinstance(data["participant"], str) and 1 <= len(data["participant"].strip()) <= 80,
        isinstance(data["unit"], str) and 1 <= len(data["unit"].strip()) <= 120,
        type(data["score"]) is int and 0 <= data["score"] <= 1000,
        type(data["total"]) is int and 1 <= data["total"] <= 1000,
        isinstance(data["completedAt"], str) and 10 <= len(data["completedAt"]) <= 40,
        isinstance(data.get("answers", []), list) and len(data.get("answers", [])) <= 100,
    ]
    if not all(checks):
        return False, "invalid-field-value"
    if data["score"] > data["total"]:
        return False, "score-exceeds-total"
    return True, "ok"


def safe_event(event: str, **fields: Any) -> None:
    """Log metadata only. Never pass participant, unit, token or raw body here."""
    record = {"event": event, **fields}
    print(json.dumps(record, ensure_ascii=False), flush=True)


class Handler(BaseHTTPRequestHandler):
    server_version = "LocalSecurityLab/1.0"

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        # Disable BaseHTTPRequestHandler access log because request lines can be noisy.
        return

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"ok": True})
        else:
            self._json(404, {"ok": False, "error": "not-found"})

    def do_POST(self) -> None:
        request_id = str(uuid.uuid4())[:8]
        if self.path != "/api/results":
            self._json(404, {"ok": False, "error": "not-found"})
            return

        expected = os.environ.get("DEMO_API_TOKEN", "")
        auth = self.headers.get("Authorization", "")
        supplied = auth.removeprefix("Bearer ") if auth.startswith("Bearer ") else ""
        if not expected or not supplied or not hmac.compare_digest(expected, supplied):
            safe_event("request.rejected", requestId=request_id, reason="unauthorized", status=401)
            self._json(401, {"ok": False, "error": "unauthorized"})
            return

        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError:
            length = MAX_BODY + 1
        if length < 0 or length > MAX_BODY:
            safe_event("request.rejected", requestId=request_id, reason="body-too-large", status=413)
            self._json(413, {"ok": False, "error": "body-too-large"})
            return

        try:
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            safe_event("request.rejected", requestId=request_id, reason="invalid-json", status=400)
            self._json(400, {"ok": False, "error": "invalid-request"})
            return

        valid, reason = validate_payload(data)
        if not valid:
            safe_event("request.rejected", requestId=request_id, reason="schema-rejected", status=400)
            self._json(400, {"ok": False, "error": "invalid-request"})
            return

        try:
            db_path = Path(os.environ.get("DEMO_DB_PATH", Path(__file__).with_name("demo_results.db")))
            conn = connect(db_path)
            try:
                row_id = insert_result(conn, data)
            finally:
                conn.close()
            safe_event(
                "result.accepted",
                requestId=request_id,
                trainerId=data["trainerId"],
                score=data["score"],
                total=data["total"],
                participantLength=len(data["participant"]),
                unitLength=len(data["unit"]),
            )
            self._json(201, {"ok": True, "id": row_id})
        except Exception as exc:
            # Diagnostic type only, no payload/token values.
            safe_event("server.error", requestId=request_id, errorType=type(exc).__name__, status=500)
            self._json(500, {"ok": False, "error": "internal-error"})


def main() -> None:
    token = os.environ.get("DEMO_API_TOKEN", "")
    if len(token) < 12:
        print("Set DEMO_API_TOKEN to a local demo value of at least 12 characters.", file=sys.stderr)
        raise SystemExit(2)
    port = int(os.environ.get("DEMO_API_PORT", "8765"))
    server = ThreadingHTTPServer((HOST, port), Handler)
    print(f"Local security lab: http://{HOST}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
