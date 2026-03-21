"""Tests de integración para POST /cases/recommendations. App real con RecommendationsUseCase y MedicationRepository in-memory (seed)."""


def test_recommendations_valid_case_returns_200_and_grouped_response(client):
    """Caso válido: 200, groups por síntoma, hasta 3 productos por grupo ordenados por margen (badge main + alternative)."""
    body = {
        "age": 35,
        "sex": "Mujer",
        "isPregnant": False,
        "symptoms": [
            {"id": "sym-1", "label": "Dolor de garganta"},
            {"id": "sym-2", "label": "Tos"},
        ],
        "hypotheses": [],
    }
    response = client.post("/cases/recommendations", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "groups" in data
    assert "explanation" in data
    assert isinstance(data["groups"], list)
    assert len(data["groups"]) == 2
    assert data["groups"][0]["symptomLabel"] == "Dolor de garganta"
    assert data["groups"][1]["symptomLabel"] == "Fiebre leve"
    for group in data["groups"]:
        recs = group["recommendations"]
        assert isinstance(recs, list)
        assert len(recs) <= 3
        if len(recs) >= 1:
            assert recs[0]["badge"] == "main"
            for item in recs[1:]:
                assert item["badge"] == "alternative"
        for item in recs:
            assert "id" in item
            assert "name" in item
            assert "category" in item
            assert "reason" in item
            assert "badge" in item
            assert "recommendedFor" in item
            assert "commercialMargin" in item
            assert "stockUnits" in item
            assert item["recommendedFor"] == group["symptomLabel"]
            assert item["commercialMargin"]
            assert item["stockUnits"]
    assert isinstance(data["explanation"], str)
    assert len(data["explanation"]) > 0


def test_recommendations_no_match_returns_200_empty_groups(client):
    """Caso sin coincidencias: grupos por síntoma con listas vacías."""
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
    assert "groups" in data
    assert len(data["groups"]) == 1
    assert data["groups"][0]["symptomLabel"] == "Síntoma inexistente en catálogo"
    assert data["groups"][0]["recommendations"] == []
    assert "explanation" in data and isinstance(data["explanation"], str)


def test_recommendations_invalid_body_returns_422(client):
    """Body inválido (tipo incorrecto en sex): 422."""
    response = client.post(
        "/cases/recommendations",
        json={"age": 35, "sex": "Invalido", "isPregnant": False, "symptoms": [], "hypotheses": []},
    )
    assert response.status_code == 422
