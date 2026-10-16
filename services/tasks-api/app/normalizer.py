import requests


class NormalizerClient:
    """Calls the title-normalizer function. Never raises: on any failure returns None."""

    def __init__(self, base_url: str, timeout: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def normalize(self, title: str):
        try:
            response = requests.post(
                f"{self.base_url}/invoke", json={"title": title}, timeout=self.timeout
            )
            response.raise_for_status()
            normalized = response.json()["title"]
        except (requests.RequestException, ValueError, KeyError, TypeError):
            return None
        return normalized if isinstance(normalized, str) else None
