"""Client for SMSGate, the outside provider that delivers the messages."""

import requests

TIMEOUT_SECONDS = 5


class RetryableError(Exception):
    """The request may succeed when it is sent again."""


class PermanentError(Exception):
    """The request will fail again, however often it is sent."""


class SmsClient:
    def __init__(self, base_url: str, token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token

    def send(self, to: str, body: str) -> str:
        """Send one message and return the provider's id for it."""
        try:
            response = requests.post(
                f"{self._base_url}/v2/messages",
                json={"to": to, "body": body},
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=TIMEOUT_SECONDS,
            )
        except requests.Timeout as error:
            raise RetryableError("timeout") from error
        if response.status_code == 429 or response.status_code >= 500:
            raise RetryableError(f"status {response.status_code}")
        if response.status_code >= 400:
            raise PermanentError(f"status {response.status_code}")
        return response.json()["id"]
