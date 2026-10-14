import pytest
from unittest.mock import AsyncMock, patch
import httpx
from weatherxm_stormwater.alerts import AlertDispatcher

def test_alert_risk_evaluation():
    dispatcher = AlertDispatcher()
    assert dispatcher.evaluate_risk(75.0) == "NORMAL"
    assert dispatcher.evaluate_risk(88.0) == "WARNING"
    assert dispatcher.evaluate_risk(105.0) == "CRITICAL"

@pytest.mark.asyncio
async def test_alert_dispatch_no_webhook():
    dispatcher = AlertDispatcher(webhook_url=None)
    result = await dispatcher.send_alert_payload("station-01", 3.2, 92.0, "WARNING")
    assert result["status"] == "skipped"
    assert result["payload"]["action_required"] is True

@pytest.mark.asyncio
async def test_alert_dispatch_success():
    dispatcher = AlertDispatcher(webhook_url="https://webhook.site/test")
    mock_response = httpx.Response(200, request=httpx.Request("POST", "https://webhook.site/test"))
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await dispatcher.send_alert_payload("station-01", 4.5, 105.0, "CRITICAL")
        assert result["status"] == "dispatched"
        assert result["http_code"] == 200

@pytest.mark.asyncio
async def test_alert_dispatch_failure():
    dispatcher = AlertDispatcher(webhook_url="https://webhook.site/test")
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.RequestError("Network timeout")
        result = await dispatcher.send_alert_payload("station-01", 4.5, 105.0, "CRITICAL")
        assert result["status"] == "failed"
        assert "Network timeout" in result["error"]