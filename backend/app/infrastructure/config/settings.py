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

    CORS_ORIGINS: str = "http://localhost:5173"
    """Orígenes permitidos para CORS (separados por coma). En desarrollo el front suele estar en 5173 (Vite) y el back en 8000."""
