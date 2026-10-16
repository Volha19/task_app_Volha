import pytest

from app import create_app


class StubNormalizer:
    """Stands in for the title-normalizer function: no network in tests."""

    def __init__(self, result="Normalized"):
        self.result = result
        self.calls = []

    def normalize(self, title):
        self.calls.append(title)
        return self.result


@pytest.fixture
def stub():
    return StubNormalizer()


@pytest.fixture
def client(stub):
    return create_app(normalizer=stub).test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_starts_empty(client):
    assert client.get("/tasks").get_json() == []


def test_create_uses_normalized_title(client, stub):
    response = client.post("/tasks", json={"title": "  buy   milk "})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "title": "Normalized", "normalized": True}
    assert stub.calls == ["  buy   milk "]


def test_create_degrades_when_function_unavailable():
    client = create_app(normalizer=StubNormalizer(result=None)).test_client()
    response = client.post("/tasks", json={"title": "  walk   dog "})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "title": "  walk   dog ", "normalized": False}


@pytest.mark.parametrize("body", [{}, {"title": ""}, {"title": "   "}, {"title": 5}, []])
def test_create_rejects_invalid_title_without_calling_function(client, stub, body):
    response = client.post("/tasks", json=body)
    assert response.status_code == 400
    assert stub.calls == []


def test_create_rejects_non_json_body(client, stub):
    response = client.post("/tasks", data="x")
    assert response.status_code == 400
    assert stub.calls == []


def test_get_and_list_return_created_tasks(client):
    client.post("/tasks", json={"title": "one"})
    client.post("/tasks", json={"title": "two"})
    assert client.get("/tasks/2").get_json()["id"] == 2
    assert [t["id"] for t in client.get("/tasks").get_json()] == [1, 2]


def test_get_unknown_task_is_404(client):
    assert client.get("/tasks/99").status_code == 404


def test_delete_removes_task_then_404(client):
    client.post("/tasks", json={"title": "one"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404
    assert client.delete("/tasks/1").status_code == 404


def test_ids_are_not_reused_after_delete(client):
    client.post("/tasks", json={"title": "one"})
    client.delete("/tasks/1")
    assert client.post("/tasks", json={"title": "two"}).get_json()["id"] == 2
