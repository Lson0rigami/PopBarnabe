from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from data.config_operacional import APP_TIMEZONE

BASE_DIR = Path(__file__).resolve().parents[1]
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = Path(os.environ.get("BARNABE_OPS_DB_PATH", INSTANCE_DIR / "barnabe_ops.sqlite3"))


def agora_local() -> datetime:
    return datetime.now(ZoneInfo(APP_TIMEZONE))


def agora_iso() -> str:
    return agora_local().isoformat(timespec="seconds")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=15000")
    return conn


@contextmanager
def connection():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _column_names(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def init_db():
    """Cria o banco e aplica migrações aditivas sem apagar dados existentes."""
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS activity_state (
                work_date TEXT NOT NULL,
                task_id TEXT NOT NULL,
                task_kind TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'available',
                started_at TEXT,
                completed_at TEXT,
                validated_at TEXT,
                blocked_at TEXT,
                contributors_json TEXT NOT NULL DEFAULT '[]',
                validator TEXT,
                note TEXT NOT NULL DEFAULT '',
                blocked_reason TEXT NOT NULL DEFAULT '',
                points_total REAL NOT NULL DEFAULT 0,
                points_each REAL NOT NULL DEFAULT 0,
                points_distribution_json TEXT NOT NULL DEFAULT '{}',
                requires_validation INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (work_date, task_id)
            );

            CREATE TABLE IF NOT EXISTS activity_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_date TEXT NOT NULL,
                task_id TEXT NOT NULL,
                task_kind TEXT NOT NULL,
                action TEXT NOT NULL,
                actor_names TEXT NOT NULL DEFAULT '',
                details_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS app_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_state_date ON activity_state(work_date);
            CREATE INDEX IF NOT EXISTS idx_events_date ON activity_events(work_date, id DESC);
            CREATE INDEX IF NOT EXISTS idx_events_task ON activity_events(work_date, task_id, id DESC);
            """
        )

        # Migração da V3 -> V4: adiciona distribuição individual de pontos.
        # ALTER TABLE é usado somente se a coluna ainda não existir, preservando
        # todos os registros já gravados no PythonAnywhere.
        columns = _column_names(conn, "activity_state")
        if "points_distribution_json" not in columns:
            conn.execute(
                "ALTER TABLE activity_state ADD COLUMN points_distribution_json TEXT NOT NULL DEFAULT '{}'"
            )


def serialize_state(row):
    if not row:
        return None
    data = dict(row)
    try:
        data["contributors"] = json.loads(data.pop("contributors_json") or "[]")
    except Exception:
        data["contributors"] = []
        data.pop("contributors_json", None)
    try:
        data["points_distribution"] = json.loads(data.pop("points_distribution_json") or "{}")
    except Exception:
        data["points_distribution"] = {}
        data.pop("points_distribution_json", None)
    data["requires_validation"] = bool(data["requires_validation"])
    return data


def get_states(work_date: str):
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM activity_state WHERE work_date=?", (work_date,)
        ).fetchall()
    return {row["task_id"]: serialize_state(row) for row in rows}


def get_state(work_date: str, task_id: str):
    with connection() as conn:
        row = conn.execute(
            "SELECT * FROM activity_state WHERE work_date=? AND task_id=?",
            (work_date, task_id),
        ).fetchone()
    return serialize_state(row)


def get_states_between(start_date: str, end_date: str):
    """Retorna estados no intervalo inclusivo; usado pelo painel individual do RH."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM activity_state WHERE work_date>=? AND work_date<=? ORDER BY work_date, task_id",
            (start_date, end_date),
        ).fetchall()
    return [serialize_state(row) for row in rows]


def upsert_state(work_date: str, task_id: str, task_kind: str, values: dict):
    now = agora_iso()
    existing = get_state(work_date, task_id)
    base = {
        "status": "available",
        "started_at": None,
        "completed_at": None,
        "validated_at": None,
        "blocked_at": None,
        "contributors": [],
        "validator": None,
        "note": "",
        "blocked_reason": "",
        "points_total": 0,
        "points_each": 0,
        "points_distribution": {},
        "requires_validation": False,
    }
    if existing:
        for key in base:
            if key in existing:
                base[key] = existing[key]
    base.update(values)

    with connection() as conn:
        conn.execute(
            """
            INSERT INTO activity_state (
                work_date, task_id, task_kind, status, started_at, completed_at,
                validated_at, blocked_at, contributors_json, validator, note,
                blocked_reason, points_total, points_each, points_distribution_json,
                requires_validation, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(work_date, task_id) DO UPDATE SET
                task_kind=excluded.task_kind,
                status=excluded.status,
                started_at=excluded.started_at,
                completed_at=excluded.completed_at,
                validated_at=excluded.validated_at,
                blocked_at=excluded.blocked_at,
                contributors_json=excluded.contributors_json,
                validator=excluded.validator,
                note=excluded.note,
                blocked_reason=excluded.blocked_reason,
                points_total=excluded.points_total,
                points_each=excluded.points_each,
                points_distribution_json=excluded.points_distribution_json,
                requires_validation=excluded.requires_validation,
                updated_at=excluded.updated_at
            """,
            (
                work_date,
                task_id,
                task_kind,
                base["status"],
                base["started_at"],
                base["completed_at"],
                base["validated_at"],
                base["blocked_at"],
                json.dumps(base["contributors"], ensure_ascii=False),
                base["validator"],
                base["note"],
                base["blocked_reason"],
                float(base["points_total"] or 0),
                float(base["points_each"] or 0),
                json.dumps(base["points_distribution"], ensure_ascii=False),
                int(bool(base["requires_validation"])),
                now,
            ),
        )
    return get_state(work_date, task_id)


def log_event(work_date: str, task_id: str, task_kind: str, action: str, actors=None, details=None):
    actors = actors or []
    details = details or {}
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO activity_events(
                work_date, task_id, task_kind, action, actor_names, details_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                work_date,
                task_id,
                task_kind,
                action,
                ", ".join(actors),
                json.dumps(details, ensure_ascii=False),
                agora_iso(),
            ),
        )


def _serialize_event(row):
    data = dict(row)
    try:
        data["details"] = json.loads(data.pop("details_json") or "{}")
    except Exception:
        data["details"] = {}
        data.pop("details_json", None)
    return data


def recent_events(work_date: str, limit=30):
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM activity_events WHERE work_date=? ORDER BY id DESC LIMIT ?",
            (work_date, int(limit)),
        ).fetchall()
    return [_serialize_event(row) for row in rows]


def get_task_events(work_date: str, task_id: str, limit=80):
    with connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM activity_events
            WHERE work_date=? AND task_id=?
            ORDER BY id DESC LIMIT ?
            """,
            (work_date, task_id, int(limit)),
        ).fetchall()
    return [_serialize_event(row) for row in rows]


def get_events_between(start_date: str, end_date: str, limit=1000):
    with connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM activity_events
            WHERE work_date>=? AND work_date<=?
            ORDER BY work_date DESC, id DESC LIMIT ?
            """,
            (start_date, end_date, int(limit)),
        ).fetchall()
    return [_serialize_event(row) for row in rows]


def get_meta(key: str, default=None):
    with connection() as conn:
        row = conn.execute("SELECT value FROM app_meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_meta(key: str, value: str):
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO app_meta(key,value) VALUES(?,?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """,
            (key, value),
        )


def event_count():
    with connection() as conn:
        return conn.execute("SELECT COUNT(*) AS n FROM activity_events").fetchone()["n"]
