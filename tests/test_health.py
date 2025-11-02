from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.json()


def test_health():
    res = client.get("/api/users/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_list_users():
    res = client.get("/api/users/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any(u.get("name") == "Alice" for u in data)
