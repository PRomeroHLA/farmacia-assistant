"""Implementación del puerto TokenService con PyJWT. Inyectable en el caso de uso de login."""

import time

import jwt

from app.application.ports.token_service import TokenService
from app.infrastructure.config import Settings


class JWTTokenService(TokenService):
    """Genera y decodifica tokens JWT. Lee JWT_SECRET_KEY y JWT_EXPIRE_MINUTES desde settings."""

    def __init__(self, settings: Settings) -> None:
        self._secret = settings.JWT_SECRET_KEY
        self._default_expiry_minutes = settings.JWT_EXPIRE_MINUTES

    def create_token(self, user_id: str, username: str, expiry_minutes: int = 60) -> str:
        exp_minutes = expiry_minutes if expiry_minutes > 0 else self._default_expiry_minutes
        now = int(time.time())
        payload = {
            "sub": user_id,
            "username": username,
            "exp": now + exp_minutes * 60,
            "iat": now,
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self._secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None
