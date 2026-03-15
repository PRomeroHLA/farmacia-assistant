"""Tests de integración para POST /cases/recommendations. App real con RecommendationsUseCase y MedicationRepository in-memory (seed)."""


def test_recommendations_valid_case_returns_200_and_recommendations_response(client):
    """Caso válido que coincide con medicamentos del seed: 200 y RecommendationsResponse con recommendations y explanation."""
    body = {
        "age": 35,
        "sex": "Mujer",
        "isPregnant": False,
        "symptoms": [
            {"id": "sym-1", "label": "Dolor de garganta"},
            {"id": "sym-2", "label": "Fiebre leve"},
        ],
        "hypotheses": [{"id": "hyp-1", "label": "Faringitis leve"}],
    }
    response = client.post("/cases/recommendations", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "explanation" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) >= 1
    assert data["recommendations"][0]["badge"] == "main"
    for item in data["recommendations"][1:]:
        assert item["badge"] == "alternative"
    for item in data["recommendations"]:
        assert "id" in item
        assert "name" in item
        assert "category" in item
        assert "reason" in item
        assert "badge" in item
    assert isinstance(data["explanation"], str)
    assert len(data["explanation"]) > 0


def test_recommendations_no_match_returns_200_empty_recommendations(client):
    """Caso que no coincide con ningún medicamento del catálogo: 200 y recommendations vacía, explanation presente."""
    body = {
        "age": 99,
        "sex": "Mujer",
        "isPregnant": False,
        "symptoms": [{"id": "x", "label": "Síntoma inexistente en catálogo"}],
        "hypotheses": [{"id": "y", "label": "Hipótesis inexistente en catálogo"}],
    }
    response = client.post("/cases/recommendations", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["recommendations"] == []
    assert "explanation" in data and isinstance(data["explanation"], str)


def test_recommendations_invalid_body_returns_422(client):
    """Body inválido (tipo incorrecto en sex): 422."""
    response = client.post(
        "/cases/recommendations",
        json={"age": 35, "sex": "Invalido", "isPregnant": False, "symptoms": [], "hypotheses": []},
    )
    assert response.status_code == 422
