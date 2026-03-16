"""Tests de integración para POST /auth/login. App real con repos in-memory y usuario de prueba (test/test123)."""


def test_login_success_returns_200_user_and_token(client):
    """Credenciales válidas (usuario test, password test123): 200, body con user (id, username, fullName) y token no vacío. Sin password_hash ni password."""
    response = client.post(
        "/auth/login",
        json={"username": "test", "password": "test123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["id"]
    assert data["user"]["username"] == "test"
    assert "fullName" in data["user"]
    assert "token" in data
    assert isinstance(data["token"], str) and len(data["token"]) > 0
    assert "password_hash" not in data
    assert "password" not in data
    assert "password_hash" not in data.get("user", {})
    assert "password" not in data.get("user", {})


def test_login_wrong_password_returns_401(client):
    """Contraseña incorrecta: 401 (o 403), sin token en body."""
    response = client.post(
        "/auth/login",
        json={"username": "test", "password": "wrong"},
    )
    assert response.status_code in (401, 403)
    data = response.json()
    assert "token" not in data or data.get("token") is None


def test_login_unknown_user_returns_401(client):
    """Usuario inexistente: 401 (o 403)."""
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "any"},
    )
    assert response.status_code in (401, 403)
