import pytest
import requests

from app.normalizer import NormalizerClient


class FakeResponse:
    def __init__(self, payload=None, status=200, json_error=False):
        self._payload = payload
        self.status = status
        self._json_error = json_error

    def raise_for_status(self):
        if self.status >= 400:
            raise requests.HTTPError(f"{self.status}")

    def json(self):
        if self._json_error:
            raise ValueError("not json")
        return self._payload


def patch_post(monkeypatch, result):
    def fake_post(url, json, timeout):
        fake_post.seen = (url, json, timeout)
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(requests, "post", fake_post)
    return fake_post


def test_success_returns_title_and_calls_invoke(monkeypatch):
    fake = patch_post(monkeypatch, FakeResponse({"title": "Buy milk"}))
    client = NormalizerClient("http://fn:5001/", timeout=0.5)
    assert client.normalize("buy milk") == "Buy milk"
    assert fake.seen == ("http://fn:5001/invoke", {"title": "buy milk"}, 0.5)


@pytest.mark.parametrize(
    "result",
    [
        requests.ConnectionError("down"),
        requests.Timeout("slow"),
        FakeResponse(status=500),
        FakeResponse(json_error=True),
        FakeResponse({}),
        FakeResponse([]),
        FakeResponse("text"),
        FakeResponse({"title": 5}),
    ],
)
def test_any_failure_returns_none(monkeypatch, result):
    patch_post(monkeypatch, result)
    assert NormalizerClient("http://fn:5001").normalize("x") is None
