from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from src.main import app
from src.dependencies.database import get_db

# Override DB dependency — no real DB needed in tests
async def override_get_db():
    yield MagicMock()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

MOCK_AUTH_TOKEN = {
    "access_token": "test_access_token",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "test_refresh_token",
}

MOCK_USER_INFO = {
    "sub": "test_esi_id",
    "name": "Test User",
    "email": "test@example.com",
    "family_name": "User",
    "given_name": "Test",
    "organization_tin": "123456789012",
    "organization_name": "Test Corp",
    "position_name": "Developer",
    "pin": "12345678901",
    "citizenship": "KZ",
    "gender": "M",
    "birthdate": "1990-01-01",
    "phone_number": "+77001234567",
}


def _mock_service(auth_token=MOCK_AUTH_TOKEN, user_info=MOCK_USER_INFO):
    mock_user = MagicMock()
    mock_user.id = 1

    mock = MagicMock()
    mock.get_auth_token = AsyncMock(return_value=auth_token)
    mock.get_user_info = AsyncMock(return_value=user_info)
    mock.get_or_create_esi_user = AsyncMock(return_value=mock_user)
    mock.save_esi_token = AsyncMock()
    return mock


def test_esi_login_success():
    with patch("src.apps.esi.router.EsiService", return_value=_mock_service()):
        response = client.post(
            "/api/v1/esi_login",
            json={"code": "test_code", "code_verifier": "test_verifier"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "test_access_token"
    assert data["esi_user_id"] == 1
    assert data["esi_user_info"]["sub"] == "test_esi_id"


def test_esi_login_missing_code_verifier():
    response = client.post("/api/v1/esi_login", json={"code": "test_code"})
    assert response.status_code == 422


def test_esi_login_esi_token_error():
    with patch("src.apps.esi.router.EsiService", return_value=_mock_service(auth_token=None)):
        response = client.post(
            "/api/v1/esi_login",
            json={"code": "test_code", "code_verifier": "test_verifier"},
        )

    assert response.status_code == 500
    assert "auth token" in response.json()["detail"]


def test_esi_login_esi_userinfo_error():
    with patch("src.apps.esi.router.EsiService", return_value=_mock_service(user_info=None)):
        response = client.post(
            "/api/v1/esi_login",
            json={"code": "test_code", "code_verifier": "test_verifier"},
        )

    assert response.status_code == 500
    assert "user info" in response.json()["detail"]
