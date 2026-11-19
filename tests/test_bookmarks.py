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
    assert client.get("/bookmarks").json() == []
    payload = {"title": "FastAPI docs", "url": "https://fastapi.tiangolo.com/"}
    saved = client.post("/bookmarks", json=payload)
    assert saved.status_code == 201
    bookmark = saved.json()
    assert UUID(bookmark["id"]).version == 4
    assert bookmark == {**payload, "id": bookmark["id"]}
    listed = client.get("/bookmarks")
    assert listed.status_code == 200
    assert listed.json() == [bookmark]


def test_duplicate_and_request_logs(client, caplog):
    caplog.set_level(logging.INFO, logger="uvicorn.error")
    saved = client.post("/bookmarks", json={"url": "https://example.org", "title": "First"})
    duplicate = client.post("/bookmarks", json={"url": "https://example.org/", "title": "Second"})
    assert saved.status_code == 201
    assert duplicate.status_code == 409
    assert client.get("/bookmarks").json() == [saved.json()]
    assert saved.headers["X-Request-ID"] != duplicate.headers["X-Request-ID"]
    for response in (saved, duplicate):
        request_id = response.headers["X-Request-ID"]
        assert UUID(request_id).version == 4
        assert f"request_id={request_id} method=POST path=/bookmarks status={response.status_code}" in caplog.messages


@pytest.mark.parametrize("url,title", [("invalid", "Example"), ("https://example.org/", "  ")])
def test_invalid_bookmark(client, url, title):
    response = client.post("/bookmarks", json={"url": url, "title": title})
    assert response.status_code == 422
    assert UUID(response.headers["X-Request-ID"]).version == 4
    assert client.get("/bookmarks").json() == []
