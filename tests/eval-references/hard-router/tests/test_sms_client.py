"""Reference result for the hard-router case: the client against stubbed HTTP responses.

SMSGate is an outside provider with no sandbox, so no test calls it, and nobody
can verify a consumer-driven contract against it.
"""

import pytest
import requests
import responses

from notify.sms_client import PermanentError, RetryableError, SmsClient

URL = "https://smsgate.test/v2/messages"


@pytest.fixture
def client():
    return SmsClient("https://smsgate.test", "token-123")


@responses.activate
def test_send_returns_the_providers_message_id(client):
    responses.post(URL, json={"id": "msg_01HZX", "status": "queued"}, status=201)
    assert client.send("+4915112345678", "hi") == "msg_01HZX"
    assert responses.calls[0].request.headers["Authorization"] == "Bearer token-123"


@pytest.mark.parametrize("status", [429, 500, 503])
@responses.activate
def test_rate_limit_and_server_errors_can_be_retried(client, status):
    responses.post(URL, status=status)
    with pytest.raises(RetryableError):
        client.send("+4915112345678", "hi")


@responses.activate
def test_timeout_can_be_retried(client):
    responses.post(URL, body=requests.Timeout())
    with pytest.raises(RetryableError):
        client.send("+4915112345678", "hi")


@pytest.mark.parametrize("status", [400, 401])
@responses.activate
def test_other_client_errors_are_permanent(client, status):
    responses.post(URL, json={"error": "invalid_number"}, status=status)
    with pytest.raises(PermanentError):
        client.send("+4915112345678", "hi")
