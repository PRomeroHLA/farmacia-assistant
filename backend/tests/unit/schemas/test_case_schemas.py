"""Tests de contrato para schemas de caso clínico. Alineados con frontend clinical.ts."""

from app.interfaces.api.schemas.case import (
    SymptomSchema,
    ClinicalHypothesisSchema,
    StructuredCaseResponse,
    AnalyzeCaseRequest,
)


def test_symptom_schema_has_id_and_label():
    """SymptomSchema: id, label (str)."""
    s = SymptomSchema(id="s1", label="Dolor de garganta")
    data = s.model_dump(by_alias=True)
    assert data["id"] == "s1"
    assert data["label"] == "Dolor de garganta"


def test_clinical_hypothesis_schema_has_id_and_label():
    """ClinicalHypothesisSchema: id, label (str)."""
    h = ClinicalHypothesisSchema(id="h1", label="Faringitis leve")
    data = h.model_dump(by_alias=True)
    assert data["id"] == "h1"
    assert data["label"] == "Faringitis leve"


def test_structured_case_response_has_expected_keys_and_types():
    """StructuredCaseResponse: age (int|null), sex ('Hombre'|'Mujer'|null), isPregnant (bool), symptoms, hypotheses."""
    resp = StructuredCaseResponse(
        age=35,
        sex="Hombre",
        is_pregnant=False,
        symptoms=[SymptomSchema(id="s1", label="Dolor de garganta")],
        hypotheses=[ClinicalHypothesisSchema(id="h1", label="Faringitis leve")],
    )
    data = resp.model_dump(by_alias=True)
    assert "age" in data
    assert data["age"] == 35
    assert "sex" in data
    assert data["sex"] == "Hombre"
    # Frontend espera isPregnant (camelCase)
    assert "isPregnant" in data
    assert data["isPregnant"] is False
    assert "symptoms" in data
    assert len(data["symptoms"]) == 1
    assert data["symptoms"][0]["id"] == "s1" and data["symptoms"][0]["label"] == "Dolor de garganta"
    assert "hypotheses" in data
    assert len(data["hypotheses"]) == 1
    assert data["hypotheses"][0]["id"] == "h1" and data["hypotheses"][0]["label"] == "Faringitis leve"


def test_structured_case_response_nullable_fields():
    """StructuredCaseResponse acepta age y sex como null."""
    resp = StructuredCaseResponse(
        age=None,
        sex=None,
        is_pregnant=False,
        symptoms=[],
        hypotheses=[],
    )
    data = resp.model_dump(by_alias=True)
    assert data["age"] is None
    assert data["sex"] is None
    assert data["isPregnant"] is False


def test_analyze_case_request_has_text_field():
    """AnalyzeCaseRequest: body con el texto del caso (campo 'text' o 'caseText')."""
    req = AnalyzeCaseRequest(text="Paciente de 35 años con dolor de garganta desde ayer.")
    data = req.model_dump(by_alias=True)
    # Convención API: un solo campo para el texto
    assert "text" in data or "caseText" in data
    text_value = data.get("text") or data.get("caseText")
    assert "dolor de garganta" in text_value
