"""Fixtures para tests. Fuerza LLM_EXTRACTOR=mock para no llamar a la API real de OpenAI."""

import os

import pytest
from starlette.testclient import TestClient

# Asegurar que los tests usen siempre el extractor mock (no OpenAI). Debe ejecutarse antes de importar app.
os.environ["LLM_EXTRACTOR"] = "mock"

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    """Cliente HTTP para tests contra la app FastAPI."""
    return TestClient(app)
