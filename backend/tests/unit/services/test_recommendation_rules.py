"""Tests unitarios para reglas de coincidencia caso–medicamento (TDD)."""

import pytest

from app.domain.entities import (
    ClinicalHypothesis,
    Medication,
    StructuredCase,
    Symptom,
)
from app.domain.services.recommendation_rules import (
    matching_recommendation_label,
    medication_matches_case,
)


def _med(**kwargs) -> Medication:
    """Medicamento mínimo para tests (solo campos obligatorios + kwargs)."""
    defaults = {
        "id": "med-1",
        "name": "Test",
        "category": "Cat",
        "reason": "R",
        "badge": "main",
    }
    defaults.update(kwargs)
    return Medication(**defaults)


def _case(
    age: int | None = None,
    sex: str | None = None,
    is_pregnant: bool = False,
    symptoms: list | None = None,
    hypotheses: list | None = None,
) -> StructuredCase:
    """Caso mínimo para tests."""
    return StructuredCase(
        age=age,
        sex=sex,
        is_pregnant=is_pregnant,
        symptoms=symptoms or [],
        hypotheses=hypotheses or [],
    )


# --- Edad ---


def test_age_within_range_matches():
    """Caso age=30, medicamento age_min=18, age_max=65 → True."""
    med = _med(age_min=18, age_max=65)
    case = _case(age=30)
    assert medication_matches_case(med, case) is True


def test_age_below_min_no_match():
    """Caso age=10, medicamento age_min=18, age_max=65 → False."""
    med = _med(age_min=18, age_max=65)
    case = _case(age=10)
    assert medication_matches_case(med, case) is False


def test_age_above_max_no_match():
    """Caso age=70, medicamento age_min=18, age_max=65 → False."""
    med = _med(age_min=18, age_max=65)
    case = _case(age=70)
    assert medication_matches_case(med, case) is False


def test_age_none_limits_matches_any_age():
    """Medicamento age_min=None, age_max=None → True para cualquier edad."""
    med = _med(age_min=None, age_max=None)
    assert medication_matches_case(med, _case(age=10)) is True
    assert medication_matches_case(med, _case(age=30)) is True
    assert medication_matches_case(med, _case(age=99)) is True


def test_case_age_none_does_not_filter_by_age():
    """Caso con age=None: no se filtra por edad (criterio pasa)."""
    med = _med(age_min=18, age_max=65)
    case = _case(age=None)
    assert medication_matches_case(med, case) is True


# --- Sexo ---


def test_sex_match_allowed():
    """Caso Hombre, medicamento allowed_sexes=('Hombre',) → True."""
    med = _med(allowed_sexes=("Hombre",))
    case = _case(sex="Hombre")
    assert medication_matches_case(med, case) is True


def test_sex_no_match():
    """Caso Hombre, medicamento allowed_sexes=('Mujer',) → False."""
    med = _med(allowed_sexes=("Mujer",))
    case = _case(sex="Hombre")
    assert medication_matches_case(med, case) is False


def test_sex_empty_allowed_matches_any():
    """Medicamento allowed_sexes=() → True para cualquier sexo del caso."""
    med = _med(allowed_sexes=())
    assert medication_matches_case(med, _case(sex="Hombre")) is True
    assert medication_matches_case(med, _case(sex="Mujer")) is True


def test_case_sex_none_does_not_filter_by_sex():
    """Caso con sex=None: no se filtra por sexo (criterio pasa)."""
    med = _med(allowed_sexes=("Mujer",))
    case = _case(sex=None)
    assert medication_matches_case(med, case) is True


# --- Embarazo ---


def test_pregnant_case_requires_suitable_for_pregnancy():
    """Caso is_pregnant=True, medicamento suitable_for_pregnancy=False → False."""
    med = _med(suitable_for_pregnancy=False)
    case = _case(is_pregnant=True)
    assert medication_matches_case(med, case) is False


def test_pregnant_case_matches_when_suitable():
    """Caso is_pregnant=True, medicamento suitable_for_pregnancy=True → True."""
    med = _med(suitable_for_pregnancy=True)
    case = _case(is_pregnant=True)
    assert medication_matches_case(med, case) is True


# --- Síntomas (por nombre/label) ---


def test_symptom_match_when_case_symptom_label_in_indicated():
    """Caso con symptom label 'Dolor', medicamento indicated_symptom_labels=('Dolor','Fiebre') → True."""
    med = _med(indicated_symptom_labels=("Dolor", "Fiebre"))
    case = _case(symptoms=[Symptom(id="s1", label="Dolor")])
    assert medication_matches_case(med, case) is True


def test_symptom_no_match_when_not_indicated():
    """Caso con symptom label 'Dolor', medicamento indicated_symptom_labels=('Tos',) → False."""
    med = _med(indicated_symptom_labels=("Tos",))
    case = _case(symptoms=[Symptom(id="s1", label="Dolor")])
    assert medication_matches_case(med, case) is False


def test_case_symptoms_empty_does_not_filter_by_symptoms():
    """Caso con symptoms=[]: no se filtra por síntomas (criterio pasa)."""
    med = _med(indicated_symptom_labels=("Dolor",))
    case = _case(symptoms=[])
    assert medication_matches_case(med, case) is True


# --- Hipótesis (por nombre/label) ---


def test_hypothesis_match_when_case_hypothesis_label_in_indicated():
    """Al menos una hipótesis del caso (por label) en indicated_hypothesis_labels del medicamento → True."""
    med = _med(indicated_hypothesis_labels=("Faringitis", "Gripe"))
    case = _case(hypotheses=[ClinicalHypothesis(id="h1", label="Faringitis")])
    assert medication_matches_case(med, case) is True


def test_hypothesis_no_match_when_none_indicated():
    """Caso con hipótesis label 'Faringitis', medicamento indicated_hypothesis_labels=('Otitis',) → False."""
    med = _med(indicated_hypothesis_labels=("Otitis",))
    case = _case(hypotheses=[ClinicalHypothesis(id="h1", label="Faringitis")])
    assert medication_matches_case(med, case) is False


def test_case_hypotheses_empty_does_not_filter_by_hypotheses():
    """Caso con hypotheses=[]: no se filtra por hipótesis (criterio pasa)."""
    med = _med(indicated_hypothesis_labels=("Faringitis",))
    case = _case(hypotheses=[])
    assert medication_matches_case(med, case) is True


# --- Combinado ---


def test_all_criteria_pass_matches():
    """Si todas las reglas aplicables pasan, devuelve True."""
    med = _med(
        age_min=18,
        age_max=65,
        allowed_sexes=("Mujer",),
        suitable_for_pregnancy=False,
        indicated_symptom_labels=("Dolor",),
        indicated_hypothesis_labels=("Faringitis",),
    )
    case = _case(
        age=30,
        sex="Mujer",
        is_pregnant=False,
        symptoms=[Symptom(id="s1", label="Dolor")],
        hypotheses=[ClinicalHypothesis(id="h1", label="Faringitis")],
    )
    assert medication_matches_case(med, case) is True


def test_one_criterion_fails_no_match():
    """Si una regla falla, devuelve False."""
    med = _med(age_min=18, age_max=65, allowed_sexes=("Hombre",))
    case = _case(age=30, sex="Mujer")  # sex no coincide
    assert medication_matches_case(med, case) is False


def test_matching_recommendation_label_prefers_first_case_symptom_when_indicated():
    """Devuelve el primer síntoma del caso que el medicamento indica."""
    med = _med(indicated_symptom_labels=("Congestión nasal", "Rinorrea"))
    case = _case(
        symptoms=[
            Symptom(id="s1", label="Fiebre"),
            Symptom(id="s2", label="Congestión nasal"),
        ],
    )
    assert matching_recommendation_label(case, med) == "Congestión nasal"


def test_matching_recommendation_label_falls_back_to_hypothesis():
    """Sin síntomas coincidentes, usa la primera hipótesis del caso indicada por el medicamento."""
    med = _med(
        indicated_symptom_labels=(),
        indicated_hypothesis_labels=("Resfriado común",),
    )
    case = _case(
        symptoms=[Symptom(id="s1", label="Otro")],
        hypotheses=[
            ClinicalHypothesis(id="h1", label="Gripe"),
            ClinicalHypothesis(id="h2", label="Resfriado común"),
        ],
    )
    assert matching_recommendation_label(case, med) == "Resfriado común"


def test_matching_recommendation_label_returns_none_when_no_overlap():
    med = _med(indicated_symptom_labels=("Tos",))
    case = _case(symptoms=[Symptom(id="s1", label="Fiebre")], hypotheses=[])
    assert matching_recommendation_label(case, med) is None
