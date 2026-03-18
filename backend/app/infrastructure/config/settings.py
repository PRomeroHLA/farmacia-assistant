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
    """Modo de persistencia:
    - "memory" (por defecto): no se abre conexión a PostgreSQL y DATABASE_URL puede ser None.
    - "postgresql": se usará PostgreSQL (async) y DATABASE_URL debe estar definida.
    """

    DATABASE_URL: str | None = None
    """URL de conexión a PostgreSQL (solo cuando STORAGE_BACKEND="postgresql").
    Formato recomendado (driver asyncpg):
      postgresql+asyncpg://user:password@localhost:5432/farmacia_db
    """

    JWT_SECRET_KEY: str = "change-me-in-production"
    """Clave secreta para firmar tokens JWT. En producción usar variable de entorno."""

    JWT_EXPIRE_MINUTES: int = 60
    """Minutos hasta que expire el token JWT."""

    CORS_ORIGINS: str = "http://localhost:5173"
    """Orígenes permitidos para CORS (separados por coma). En desarrollo el front suele estar en 5173 (Vite) y el back en 8000."""

    # OpenAI e extractor LLM (video-08)
    OPENAI_API_KEY: str | None = None
    """Clave de API de OpenAI. Obligatoria cuando LLM_EXTRACTOR=openai."""

    OPENAI_MODEL: str = "gpt-4o-mini"
    """Modelo de OpenAI (p. ej. gpt-4o-mini, gpt-3.5-turbo). Puede sobrescribirse por variable de entorno."""

    LLM_EXTRACTOR: Literal["mock", "openai"] = "mock"
    """Implementación de CaseStructureExtractor: 'mock' (MockCaseStructureExtractor) o 'openai' (LangChain/OpenAI). Por defecto 'mock' para que la app funcione sin OPENAI_API_KEY y los tests usen mock."""

    def model_post_init(self, __context) -> None:  # type: ignore[override]
        # If an OpenAI key is provided and extractor wasn't explicitly switched,
        # default to OpenAI so Docker/production behaves as expected.
        if self.LLM_EXTRACTOR == "mock" and self.OPENAI_API_KEY and self.OPENAI_API_KEY.strip():
            self.LLM_EXTRACTOR = "openai"
