import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Cliente HTTP para tests contra la app FastAPI."""
    return TestClient(app)
