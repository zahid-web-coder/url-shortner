import pytest
from app.main import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_shorten_url_valid(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 201
    assert "short_code" in res.json
    assert "short_url" in res.json

def test_shorten_url_invalid(client):
    res = client.post("/api/shorten", json={"url": "invalid-url"})
    assert res.status_code == 400
    assert res.json["error"] == "Invalid URL"

def test_shorten_url_missing(client):
    res = client.post("/api/shorten", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Invalid URL"

def test_redirect_and_stats(client):
   
    res = client.post("/api/shorten", json={"url": "https://example.com/test"})
    short_code = res.json["short_code"]

    
    redirect_res = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["Location"] == "https://example.com/test"


    stats = client.get(f"/api/stats/{short_code}")
    assert stats.status_code == 200
    assert stats.json["clicks"] == 1
    assert stats.json["url"] == "https://example.com/test"
