import logging
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as client:
        yield client


def test_save_and_list(client):
    assert client.get("/users").json() == []
    payload = {"username": "ada", "display_name": "Ada Lovelace"}
    saved = client.post("/users", json=payload)
    assert saved.status_code == 201
    user = saved.json()
    assert UUID(user["id"]).version == 4
    assert user == {**payload, "id": user["id"]}
    listed = client.get("/users")
    assert listed.status_code == 200
    assert listed.json() == [user]


def test_duplicate_and_request_logs(client, caplog):
    caplog.set_level(logging.INFO, logger="uvicorn.error")
    saved = client.post("/users", json={"username": "Ada", "display_name": "Ada Lovelace"})
    duplicate = client.post("/users", json={"username": "ada", "display_name": "Second"})
    assert saved.status_code == 201
    assert duplicate.status_code == 409
    assert client.get("/users").json() == [saved.json()]
    assert saved.headers["X-Request-ID"] != duplicate.headers["X-Request-ID"]
    for response in (saved, duplicate):
        request_id = response.headers["X-Request-ID"]
        assert UUID(request_id).version == 4
        assert f"request_id={request_id} method=POST path=/users status={response.status_code}" in caplog.messages


@pytest.mark.parametrize("username,display_name", [("two words", "Example"), ("ada", "  ")])
def test_invalid_user(client, username, display_name):
    response = client.post("/users", json={"username": username, "display_name": display_name})
    assert response.status_code == 422
    assert UUID(response.headers["X-Request-ID"]).version == 4
    assert client.get("/users").json() == []
