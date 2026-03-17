"""Verifica que el usuario de prueba para login existe y el hash es válido."""

import pytest

from app.domain.entities import User
from app.infrastructure.persistence.memory import InMemoryUserRepository
from app.infrastructure.security.password import hash_password, verify_password


@pytest.mark.asyncio
async def test_seed_user_stored_with_password_hash():
    """InMemoryUserRepository almacena User con password_hash; get_by_username lo devuelve."""
    test_hash = hash_password("test123")
    repo = InMemoryUserRepository(
        initial_users=[
            User(id="test-1", username="test", full_name="Usuario de prueba", password_hash=test_hash),
        ]
    )
    user = await repo.get_by_username("test")
    assert user is not None
    assert user.username == "test"
    assert user.password_hash is not None
    assert verify_password("test123", user.password_hash) is True


def test_seed_user_password_verifies():
    """El mismo hash generado por hash_password es verificado por verify_password (login)."""
    plain = "test123"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False
