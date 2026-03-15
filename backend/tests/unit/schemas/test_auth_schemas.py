"""Tests de contrato para schemas de auth. Alineados con frontend src/shared/types (User, LoginResult)."""

from app.interfaces.api.schemas.auth import LoginRequest, LoginResponse, UserSchema


def test_login_request_has_username_and_password():
    """LoginRequest debe tener username y password (str)."""
    req = LoginRequest(username="farm", password="secret")
    data = req.model_dump(by_alias=True)
    assert "username" in data
    assert data["username"] == "farm"
    assert "password" in data
    assert data["password"] == "secret"


def test_login_response_has_user_and_optional_token():
    """LoginResponse debe tener 'user' (objeto con id, username, fullName opcional) y 'token' (str opcional)."""
    resp = LoginResponse(
        user=UserSchema(id="1", username="farm", full_name="Farmacia Centro"),
        token="jwt-token-123",
    )
    data = resp.model_dump(by_alias=True)
    assert "user" in data
    assert data["user"]["id"] == "1"
    assert data["user"]["username"] == "farm"
    # Frontend espera fullName (camelCase)
    assert "fullName" in data["user"] or "full_name" in data["user"]
    assert data["user"].get("fullName") == "Farmacia Centro" or data["user"].get("full_name") == "Farmacia Centro"
    assert "token" in data
    assert data["token"] == "jwt-token-123"


def test_login_response_user_serializes_camelCase_fullName():
    """Serialización a JSON debe producir fullName en camelCase para el frontend."""
    resp = LoginResponse(
        user=UserSchema(id="1", username="farm", full_name="Farmacia"),
        token=None,
    )
    data = resp.model_dump(by_alias=True)
    assert "user" in data
    # El frontend espera fullName (camelCase)
    assert "fullName" in data["user"]
