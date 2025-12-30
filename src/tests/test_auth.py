from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_create_user():
    response = client.post("/api/v1/token", data={"username": "harika", "password": "harika1997"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_user_me():
    token_response = client.post("/api/v1/token", data={"username": "harika", "password": "harika1997"})
    token = token_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get("username") == "harika"
