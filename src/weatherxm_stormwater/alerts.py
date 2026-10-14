"""Alert dispatcher and webhook notification engine for stormwater risks."""
from __future__ import annotations

import httpx
from typing import Any, Dict, Optional


class AlertDispatcher:
    """Evaluates hydraulic thresholds and dispatches webhook notifications."""

    def __init__(self, webhook_url: Optional[str] = None, timeout: float = 5.0) -> None:
        self.webhook_url = webhook_url
        self.timeout = timeout

    def evaluate_risk(self, capacity_utilization: float) -> str:
        if capacity_utilization >= 100.0:
            return "CRITICAL"
        if capacity_utilization >= 85.0:
            return "WARNING"
        return "NORMAL"

    async def send_alert_payload(
        self,
        station_id: str,
        discharge: float,
        capacity_utilization: float,
        risk_level: str,
    ) -> Dict[str, Any]:
        payload = {
            "station_id": station_id,
            "risk_level": risk_level,
            "discharge_m3s": round(discharge, 2),
            "capacity_utilization_pct": round(capacity_utilization, 1),
            "action_required": risk_level in ("WARNING", "CRITICAL"),
        }

        if not self.webhook_url:
            return {"status": "skipped", "reason": "no_webhook_configured", "payload": payload}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(self.webhook_url, json=payload)
                return {"status": "dispatched", "http_code": res.status_code, "payload": payload}
        except Exception as e:
            return {"status": "failed", "error": str(e), "payload": payload}