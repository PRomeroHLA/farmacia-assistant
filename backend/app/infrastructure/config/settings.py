from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    STORAGE_BACKEND: Literal["memory", "postgresql"] = "memory"
    """Modo de persistencia: "memory" (por defecto) o "postgresql"."""

    DATABASE_URL: str | None = None
    """URL de conexión a PostgreSQL. Solo necesaria cuando STORAGE_BACKEND=postgresql."""

    JWT_SECRET_KEY: str = "change-me-in-production"
    """Clave secreta para firmar tokens JWT. En producción usar variable de entorno."""

    JWT_EXPIRE_MINUTES: int = 60
    """Minutos hasta que expire el token JWT."""
