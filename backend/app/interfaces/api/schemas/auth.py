"""Schemas Pydantic para auth. Salida en camelCase para el frontend."""

from pydantic import BaseModel, ConfigDict, Field


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
