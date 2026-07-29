"""SQLite index. Lives inside the footage folder's .analysis_cache alongside
the proxies, so a batch of footage carries its own index with it."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import DB_NAME, PROXY_DIRNAME

SCHEMA = """
CREATE TABLE IF NOT EXISTS clips (
    hash TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    filename TEXT NOT NULL,
    duration REAL, fps REAL, width INTEGER, height INTEGER,
    codec TEXT, created TEXT,
    sharpness REAL, sharpness_low REAL,
    highlight_clip REAL, shadow_clip REAL,
    hue REAL, saturation REAL, brightness REAL,
    pan_rate REAL, tx_rate REAL, ty_rate REAL,
    rot_rate REAL, zoom_rate REAL,
    motion_energy REAL, confidence REAL,
    move_type TEXT
);
"""


def open_db(root: Path) -> sqlite3.Connection:
    cache = root / PROXY_DIRNAME
    cache.mkdir(exist_ok=True)
    conn = sqlite3.connect(cache / DB_NAME)
    conn.executescript(SCHEMA)
    return conn


def upsert(conn, row: dict) -> None:
    cols = ", ".join(row)
    marks = ", ".join("?" for _ in row)
    conn.execute(
        f"INSERT OR REPLACE INTO clips ({cols}) VALUES ({marks})", list(row.values())
    )
