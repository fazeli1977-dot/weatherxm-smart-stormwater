import pytest
from typer.testing import CliRunner
from weatherxm_smart_stormwater.cli import app
from weatherxm_smart_stormwater.client import WeatherXMClient
from weatherxm_smart_stormwater.models import WeatherObservation

runner = CliRunner()

@pytest.mark.asyncio
async def test_client_fallback_observation():
    client = WeatherXMClient()
    obs = await client.get_station_observation("test-station-42")
    assert isinstance(obs, WeatherObservation)
    assert obs.precipitation_rate_mm_h > 0
    assert "test-station-42" in obs.station_id

def test_cli_execution():
    result = runner.invoke(app, ["--station-id", "test-node", "--area", "25", "--runoff-c", "0.6", "--capacity", "2.0"])
    assert result.exit_code == 0
    assert "WeatherXM Smart Stormwater Infrastructure" in result.stdout
