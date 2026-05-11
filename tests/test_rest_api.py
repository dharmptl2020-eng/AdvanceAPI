import pytest
from fastapi.testclient import TestClient
from rest_apis import main as rest_main

client = TestClient(rest_main.app)

@pytest.fixture(autouse=True)
def reset_posts_db():
    rest_main.posts_db.clear()
    rest_main.post_counter = 0
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_and_get_post():
    payload = {
        "title": "Hello World",
        "content": "This is the first blog post content.",
        "author": "Alice",
        "tags": ["intro", "test"]
    }

    create_response = client.post("/posts", json=payload)
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["id"] == 1
    assert created["title"] == payload["title"]

    get_response = client.get("/posts/1")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == 1

def test_update_post():
    payload = {
        "title": "Hello World",
        "content": "This is the first blog post content.",
        "author": "Alice",
        "tags": ["intro", "test"]
    }
    client.post("/posts", json=payload)

    update_payload = {
        "title": "Updated Title",
        "content": "Updated content for the same post.",
        "author": "Alice",
        "tags": ["update"]
    }
    response = client.put("/posts/1", json=update_payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_post():
    payload = {
        "title": "Hello World",
        "content": "This is the first blog post content.",
        "author": "Alice",
        "tags": ["intro", "test"]
    }
    client.post("/posts", json=payload)

    delete_response = client.delete("/posts/1")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Post deleted successfully"

    not_found = client.get("/posts/1")
    assert not_found.status_code == 404
