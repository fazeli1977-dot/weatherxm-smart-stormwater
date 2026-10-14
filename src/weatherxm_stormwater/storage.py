"""SQLite storage engine for storm events and hydrologic telemetry."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class TelemetryStorage:
    def __init__(self, db_path: str | Path = "stormwater_telemetry.db") -> None:
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    station_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    precipitation_rate REAL NOT NULL,
                    discharge REAL NOT NULL,
                    capacity_utilization REAL NOT NULL,
                    risk_level TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def record_observation(
        self,
        station_id: str,
        precipitation_rate: float,
        discharge: float,
        capacity_utilization: float,
        risk_level: str,
        timestamp: datetime | None = None,
    ) -> int:
        ts = (timestamp or datetime.now(timezone.utc)).isoformat()
        with self._get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO observations (station_id, timestamp, precipitation_rate, discharge, capacity_utilization, risk_level)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (station_id, ts, precipitation_rate, discharge, capacity_utilization, risk_level),
            )
            conn.commit()
            return int(cur.lastrowid or 0)

    def get_recent_history(self, station_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT station_id, timestamp, precipitation_rate, discharge, capacity_utilization, risk_level
                FROM observations
                WHERE station_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (station_id, limit),
            ).fetchall()
            return [dict(row) for row in rows]