import pytest
import httpx
from typer.testing import CliRunner
from weatherxm_smart_stormwater.cli import app
from weatherxm_smart_stormwater.client import WeatherXMClient
from weatherxm_smart_stormwater.models import WeatherObservation
from unittest.mock import AsyncMock, patch

runner = CliRunner()

@pytest.mark.asyncio
async def test_client_fallback_observation():
    client = WeatherXMClient()
    obs = await client.get_station_observation("test-station-42")
    assert isinstance(obs, WeatherObservation)
    assert obs.data_source == "simulated"
    assert obs.precipitation_rate_mm_h > 0
    assert "test-station-42" in obs.station_id

@pytest.mark.asyncio
async def test_client_sends_weatherxm_api_key():
    client = WeatherXMClient(api_key="test-api-key")
    response = httpx.Response(
        200,
        json={
            "name": "Test station",
            "current_weather": {
                "precipitation_rate": 1.2,
                "precipitation_accumulated": 2.3,
                "temperature": 18.0,
                "wind_speed": 3.0,
            },
            "battery_level": 90,
        },
        request=httpx.Request("GET", "https://api.weatherxm.com/api/v1/cells/test/current"),
    )

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = response
        observation = await client.get_station_observation("test")

    assert observation.name == "Test station"
    assert observation.data_source == "live_api"
    assert mock_get.await_args.kwargs["headers"] == {"X-API-KEY": "test-api-key"}

def test_cli_execution():
    result = runner.invoke(app, ["--station-id", "test-node", "--area", "25", "--runoff-c", "0.6", "--capacity", "2.0"])
    assert result.exit_code == 0
    assert "WeatherXM Smart Stormwater Infrastructure" in result.stdout
