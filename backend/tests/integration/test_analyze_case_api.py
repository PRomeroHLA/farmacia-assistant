"""Tests de integración para POST /cases/analyze. App real con MockCaseStructureExtractor inyectado."""

from app.main import app

# Usa el client de conftest (TestClient(app)). AnalyzeCaseUseCase usa MockCaseStructureExtractor.


def test_analyze_case_returns_200_with_structured_case_response(client):
    """Body con texto: respuesta 200; body con age, sex, isPregnant, symptoms, hypotheses (claves esperadas por frontend)."""
    response = client.post(
        "/cases/analyze",
        json={"text": "Mujer 35 años, dolor de garganta desde hace 2 días"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "age" in data
    assert "sex" in data
    assert "isPregnant" in data
    assert "symptoms" in data
    assert "hypotheses" in data
    # Mock devuelve age=35, sex="Mujer", is_pregnant=False y listas no vacías
    assert data["age"] == 35
    assert data["sex"] == "Mujer"
    assert data["isPregnant"] is False
    assert isinstance(data["symptoms"], list)
    assert isinstance(data["hypotheses"], list)
    if data["symptoms"]:
        assert "id" in data["symptoms"][0] and "label" in data["symptoms"][0]
    if data["hypotheses"]:
        assert "id" in data["hypotheses"][0] and "label" in data["hypotheses"][0]


def test_analyze_case_missing_text_returns_422(client):
    """Body vacío o sin campo text → 422 (validación Pydantic)."""
    response = client.post("/cases/analyze", json={})
    assert response.status_code == 422
