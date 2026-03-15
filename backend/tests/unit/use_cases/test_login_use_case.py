"""Tests unitarios para el caso de uso de login (TDD). Solo puertos inyectados (mocks)."""

import pytest
from unittest.mock import Mock

from app.domain.entities import User
from app.application.use_cases.login import LoginUseCase, InvalidCredentialsError


@pytest.fixture
def user_repo():
    """Mock de UserRepository."""
    return Mock()


@pytest.fixture
def password_hasher():
    """Mock de PasswordHasher."""
    return Mock()


@pytest.fixture
def token_service():
    """Mock de TokenService."""
    return Mock()


@pytest.fixture
def login_use_case(user_repo, password_hasher, token_service):
    """Caso de uso con dependencias mockeadas."""
    return LoginUseCase(
        user_repository=user_repo,
        password_hasher=password_hasher,
        token_service=token_service,
    )


@pytest.fixture
def sample_user():
    """Usuario de prueba con password_hash."""
    return User(
        id="user-1",
        username="test",
        full_name="Usuario de prueba",
        password_hash="$2b$12$fakehash",
    )


def test_login_fails_when_user_does_not_exist(login_use_case, user_repo):
    """Cuando get_by_username devuelve None, el caso de uso debe indicar error."""
    user_repo.get_by_username.return_value = None

    with pytest.raises(InvalidCredentialsError):
        login_use_case.run(username="unknown", password="any")

    user_repo.get_by_username.assert_called_once_with("unknown")
    login_use_case.password_hasher.verify_password.assert_not_called()
    login_use_case.token_service.create_token.assert_not_called()


def test_login_fails_when_password_is_incorrect(
    login_use_case, user_repo, password_hasher, sample_user
):
    """Cuando el usuario existe pero verify_password devuelve False, debe indicar error."""
    user_repo.get_by_username.return_value = sample_user
    password_hasher.verify_password.return_value = False

    with pytest.raises(InvalidCredentialsError):
        login_use_case.run(username="test", password="wrong")

    user_repo.get_by_username.assert_called_once_with("test")
    password_hasher.verify_password.assert_called_once_with("wrong", sample_user.password_hash)
    login_use_case.token_service.create_token.assert_not_called()


def test_login_returns_user_and_token_when_credentials_valid(
    login_use_case, user_repo, password_hasher, token_service, sample_user
):
    """Cuando el usuario existe y la contraseña es correcta: devolver (User, token)."""
    user_repo.get_by_username.return_value = sample_user
    password_hasher.verify_password.return_value = True
    token_service.create_token.return_value = "jwt-token-123"

    user, token = login_use_case.run(username="test", password="test123")

    assert user is sample_user
    assert token == "jwt-token-123"
    user_repo.get_by_username.assert_called_once_with("test")
    password_hasher.verify_password.assert_called_once_with("test123", sample_user.password_hash)
    token_service.create_token.assert_called_once_with(
        sample_user.id, sample_user.username
    )
