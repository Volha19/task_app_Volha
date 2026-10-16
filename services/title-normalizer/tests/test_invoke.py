import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("  buy   milk ", "Buy milk"),
        ("already Fine", "Already Fine"),
        ("ŁÓDŹ trip", "ŁÓDŹ trip"),
        ("a\tb\nc", "A b c"),
        ("   ", ""),
        ("", ""),
    ],
)
def test_invoke_normalizes_title(client, raw, expected):
    response = client.post("/invoke", json={"title": raw})
    assert response.status_code == 200
    assert response.get_json() == {"title": expected}


@pytest.mark.parametrize("body", [{}, {"title": 5}, {"title": None}, [], "text"])
def test_invoke_rejects_non_string_title(client, body):
    response = client.post("/invoke", json=body)
    assert response.status_code == 400


def test_invoke_rejects_non_json_body(client):
    response = client.post("/invoke", data="x")
    assert response.status_code == 400
