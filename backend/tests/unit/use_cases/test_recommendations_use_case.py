"""Tests unitarios para el caso de uso de recomendaciones (TDD)."""

from decimal import Decimal

from app.domain.entities import (
    ClinicalHypothesis,
    Medication,
    StructuredCase,
    Symptom,
)
from app.application.use_cases.recommendations import RecommendationsUseCase
from app.infrastructure.persistence.memory import InMemoryMedicationRepository


def _case(
    age: int | None = 30,
    sex: str = "Mujer",
    is_pregnant: bool = False,
    symptoms: list | None = None,
    hypotheses: list | None = None,
) -> StructuredCase:
    return StructuredCase(
        age=age,
        sex=sex,
        is_pregnant=is_pregnant,
        symptoms=symptoms or [Symptom(id="sym-1", label="Dolor de garganta")],
        hypotheses=hypotheses or [ClinicalHypothesis(id="hyp-1", label="Faringitis leve")],
    )


def _med(
    id: str = "med-1",
    stock: str | None = "10",
    economic_margin: Decimal = Decimal("0"),
    indicated_symptom_labels: tuple = ("Dolor de garganta",),
    indicated_hypothesis_labels: tuple = ("Faringitis leve",),
    **kwargs,
) -> Medication:
    defaults = {
        "name": "Test",
        "category": "Cat",
        "reason": "R",
        "badge": "main",
        "indicated_symptom_labels": indicated_symptom_labels,
        "indicated_hypothesis_labels": indicated_hypothesis_labels,
        "economic_margin": economic_margin,
        "stock": stock,
    }
    defaults.update(kwargs)
    return Medication(id=id, **defaults)


def test_returns_matching_medications_sorted_by_margin_main_and_alternatives():
    """Dado un caso y repo con varios medicamentos (con stock, algunos coinciden), devuelve solo los que pasan reglas, ordenados por economic_margin desc, máx 5; primero 'main', resto 'alternative'."""
    med_low = _med("m1", economic_margin=Decimal("1.0"))
    med_high = _med("m2", economic_margin=Decimal("3.0"))
    med_mid = _med("m3", economic_margin=Decimal("2.0"))
    # No coincide con el caso (síntoma distinto)
    med_no_match = _med("m4", economic_margin=Decimal("5.0"), indicated_symptom_labels=("Otro síntoma",))
    repo = InMemoryMedicationRepository([med_low, med_high, med_mid, med_no_match])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case()

    result = use_case.run(case)

    assert len(result) == 3
    assert result[0].badge == "main"
    assert result[0].id == "m2"
    assert result[0].economic_margin == Decimal("3.0")
    assert result[1].badge == "alternative"
    assert result[1].id == "m3"
    assert result[2].badge == "alternative"
    assert result[2].id == "m1"


def test_returns_empty_when_no_medication_matches():
    """Si ningún medicamento coincide con el caso, devuelve lista vacía."""
    med = _med(indicated_symptom_labels=("Otro",), indicated_hypothesis_labels=("Otra hipótesis",))
    repo = InMemoryMedicationRepository([med])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case()

    result = use_case.run(case)

    assert result == []


def test_only_considers_available_medications_with_stock():
    """Solo se consideran medicamentos con stock (get_available()); uno sin stock no aparece aunque coincida."""
    med_with_stock = _med("m1", stock="5")
    med_no_stock = _med("m2", stock="0")
    repo = InMemoryMedicationRepository([med_with_stock, med_no_stock])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case()

    result = use_case.run(case)

    assert len(result) == 1
    assert result[0].id == "m1"
