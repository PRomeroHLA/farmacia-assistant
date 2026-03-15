"""Tests unitarios para el caso de uso de análisis de caso (TDD). Solo puerto CaseStructureExtractor inyectado (mock)."""

import pytest
from unittest.mock import Mock

from app.domain.entities import ClinicalHypothesis, StructuredCase, Symptom
from app.application.use_cases.analyze_case import AnalyzeCaseUseCase


@pytest.fixture
def fixed_structured_case():
    """StructuredCase fijo que devolverá el mock del extractor."""
    return StructuredCase(
        age=40,
        sex="Hombre",
        is_pregnant=False,
        symptoms=[
            Symptom(id="s1", label="Cefalea"),
        ],
        hypotheses=[
            ClinicalHypothesis(id="h1", label="Cefalea tensional"),
        ],
    )


@pytest.fixture
def mock_extractor(fixed_structured_case):
    """Mock de CaseStructureExtractor que devuelve un StructuredCase fijo."""
    extractor = Mock()
    extractor.extract.return_value = fixed_structured_case
    return extractor


@pytest.fixture
def analyze_case_use_case(mock_extractor):
    """Caso de uso con extractor mockeado (inyección)."""
    return AnalyzeCaseUseCase(case_structure_extractor=mock_extractor)


def test_analyze_case_returns_structured_case_from_extractor(
    analyze_case_use_case, mock_extractor, fixed_structured_case
):
    """Cuando el extractor devuelve un StructuredCase concreto, el caso de uso devuelve ese mismo StructuredCase."""
    text = "Paciente de 40 años con dolor de cabeza desde hace dos días."
    result = analyze_case_use_case.run(text)

    assert result is fixed_structured_case
    mock_extractor.extract.assert_called_once_with(text)
