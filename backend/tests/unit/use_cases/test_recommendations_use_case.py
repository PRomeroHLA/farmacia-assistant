"""Tests unitarios para el caso de uso de recomendaciones (TDD)."""

from decimal import Decimal

import pytest

from app.domain.entities import (
    ClinicalHypothesis,
    Medication,
    StructuredCase,
    Symptom,
)
from app.application.use_cases.recommendations import (
    PRODUCTS_PER_SYMPTOM,
    RecommendationsUseCase,
)
from app.infrastructure.persistence.memory import InMemoryMedicationRepository


def _case(
    age: int | None = 30,
    sex: str = "Mujer",
    is_pregnant: bool = False,
    symptoms: list | None = None,
    hypotheses: list | None = None,
) -> StructuredCase:
    default_symptoms = [Symptom(id="sym-1", label="Dolor de garganta")]
    default_hypotheses = [ClinicalHypothesis(id="hyp-1", label="Faringitis leve")]
    return StructuredCase(
        age=age,
        sex=sex,
        is_pregnant=is_pregnant,
        symptoms=default_symptoms if symptoms is None else symptoms,
        hypotheses=default_hypotheses if hypotheses is None else hypotheses,
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


@pytest.mark.asyncio
async def test_one_group_per_symptom_three_products_ordered_by_margin():
    """Por cada síntoma del caso: hasta 3 medicamentos indicados para ese síntoma, margen desc; primer badge main."""
    med_a = _med("m1", economic_margin=Decimal("1.0"), indicated_symptom_labels=("Tos",))
    med_b = _med("m2", economic_margin=Decimal("5.0"), indicated_symptom_labels=("Tos",))
    med_c = _med("m3", economic_margin=Decimal("3.0"), indicated_symptom_labels=("Tos",))
    med_d = _med("m4", economic_margin=Decimal("10.0"), indicated_symptom_labels=("Fiebre",))
    med_e = _med("m5", economic_margin=Decimal("2.0"), indicated_symptom_labels=("Fiebre",))
    repo = InMemoryMedicationRepository([med_a, med_b, med_c, med_d, med_e])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case(
        symptoms=[
            Symptom(id="s1", label="Tos"),
            Symptom(id="s2", label="Fiebre"),
        ],
    )

    groups = await use_case.run(case)

    assert len(groups) == 2
    assert groups[0].symptom_label == "Tos"
    assert [m.id for m in groups[0].medications] == ["m2", "m3", "m1"]
    assert groups[0].medications[0].badge == "main"
    assert groups[0].medications[1].badge == "alternative"
    assert groups[0].medications[2].badge == "alternative"

    assert groups[1].symptom_label == "Fiebre"
    assert [m.id for m in groups[1].medications] == ["m4", "m5"]
    assert groups[1].medications[0].badge == "main"
    assert groups[1].medications[1].badge == "alternative"


@pytest.mark.asyncio
async def test_limits_to_products_per_symptom():
    meds = [
        _med(f"m{i}", economic_margin=Decimal(str(i)), indicated_symptom_labels=("Tos",))
        for i in range(1, 8)
    ]
    repo = InMemoryMedicationRepository(meds)
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case(symptoms=[Symptom(id="s1", label="Tos")])

    groups = await use_case.run(case)

    assert len(groups) == 1
    assert len(groups[0].medications) == PRODUCTS_PER_SYMPTOM
    margins = [m.economic_margin for m in groups[0].medications]
    assert margins == sorted(margins, reverse=True)


@pytest.mark.asyncio
async def test_no_symptoms_falls_back_to_global_top_three_by_margin():
    med_low = _med("m1", economic_margin=Decimal("1.0"))
    med_high = _med("m2", economic_margin=Decimal("4.0"))
    med_mid = _med("m3", economic_margin=Decimal("2.0"))
    repo = InMemoryMedicationRepository([med_low, med_high, med_mid])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case(symptoms=[], hypotheses=[])

    groups = await use_case.run(case)

    assert len(groups) == 1
    assert groups[0].symptom_label is None
    assert [m.id for m in groups[0].medications] == ["m2", "m3", "m1"]


@pytest.mark.asyncio
async def test_returns_empty_groups_when_no_medication_matches_symptom():
    med = _med(indicated_symptom_labels=("Otro",), indicated_hypothesis_labels=("Otra hipótesis",))
    repo = InMemoryMedicationRepository([med])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case(symptoms=[Symptom(id="s1", label="Dolor de garganta")])

    groups = await use_case.run(case)

    assert len(groups) == 1
    assert groups[0].symptom_label == "Dolor de garganta"
    assert groups[0].medications == ()


@pytest.mark.asyncio
async def test_only_considers_available_medications_with_stock():
    """Solo se consideran medicamentos con stock (get_available()); uno sin stock no aparece."""
    med_with_stock = _med("m1", stock="5", economic_margin=Decimal("2"), indicated_symptom_labels=("Tos",))
    med_no_stock = _med("m2", stock="0", economic_margin=Decimal("9"), indicated_symptom_labels=("Tos",))
    repo = InMemoryMedicationRepository([med_with_stock, med_no_stock])
    use_case = RecommendationsUseCase(medication_repository=repo)
    case = _case(symptoms=[Symptom(id="s1", label="Tos")])

    groups = await use_case.run(case)

    assert len(groups[0].medications) == 1
    assert groups[0].medications[0].id == "m1"
