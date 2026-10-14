import pytest
from datetime import datetime, timezone
from weatherxm_stormwater.storage import TelemetryStorage
from weatherxm_stormwater.api_client import WeatherXMClient

def test_telemetry_storage_lifecycle(tmp_path):
    db_file = tmp_path / "test_storm.db"
    store = TelemetryStorage(db_file)

    row_id = store.record_observation(
        station_id="test-station-42",
        precipitation_rate=45.0,
        discharge=4.12,
        capacity_utilization=117.7,
        risk_level="CRITICAL",
        timestamp=datetime(2026, 10, 14, 12, 0, 0, tzinfo=timezone.utc),
    )
    assert row_id == 1

    records = store.get_recent_history("test-station-42", limit=10)
    assert len(records) == 1
    rec = records[0]
    assert rec["station_id"] == "test-station-42"
    assert rec["precipitation_rate"] == 45.0
    assert rec["risk_level"] == "CRITICAL"

@pytest.mark.asyncio
async def test_weatherxm_client_fallback_mode():
    client = WeatherXMClient(base_url="https://invalid-non-existent-domain.internal")
    data = await client.get_station_latest("station-mock-99")
    assert data["station_id"] == "station-mock-99"
    assert data["status"] == "SIMULATED_FEED"
    assert data["source"] == "fallback"
    assert "precipitation_rate" in data