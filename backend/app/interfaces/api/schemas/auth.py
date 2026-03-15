"""Schemas Pydantic para auth. Salida en camelCase para el frontend."""

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import User


class LoginRequest(BaseModel):
    """Cuerpo de la petición de login."""

    username: str
    password: str


class UserSchema(BaseModel):
    """Usuario en respuestas API. fullName en camelCase para el frontend."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    username: str
    full_name: str | None = Field(None, alias="fullName")


class LoginResponse(BaseModel):
    """Respuesta del login. user + token opcional."""

    model_config = ConfigDict(populate_by_name=True)

    user: UserSchema
    token: str | None = None


def user_to_schema(user: User) -> UserSchema:
    """Mapea la entidad User al schema de API. No incluye password_hash (nunca se expone)."""
    return UserSchema(id=user.id, username=user.username, full_name=user.full_name)
