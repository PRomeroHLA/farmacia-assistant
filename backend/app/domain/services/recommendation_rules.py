"""Reglas de coincidencia caso–medicamento para el motor de recomendaciones."""

from app.domain.entities import Medication, StructuredCase


def medication_matches_case(medication: Medication, case: StructuredCase) -> bool:
    """True si el medicamento es adecuado para el caso según edad, sexo, embarazo, síntomas e hipótesis.
    Si el caso no tiene edad/sexo/síntomas/hipótesis, ese criterio no se exige (no excluye).
    """
    if case.age is not None:
        if medication.age_min is not None and case.age < medication.age_min:
            return False
        if medication.age_max is not None and case.age > medication.age_max:
            return False

    if case.sex is not None and len(medication.allowed_sexes) > 0:
        if case.sex not in medication.allowed_sexes:
            return False

    if case.is_pregnant and not medication.suitable_for_pregnancy:
        return False

    if case.symptoms:
        case_symptom_labels = {s.label for s in case.symptoms}
        if not case_symptom_labels.intersection(set(medication.indicated_symptom_labels)):
            return False

    if case.hypotheses:
        case_hypothesis_labels = {h.label for h in case.hypotheses}
        if not case_hypothesis_labels.intersection(set(medication.indicated_hypothesis_labels)):
            return False

    return True


def matching_recommendation_label(case: StructuredCase, medication: Medication) -> str | None:
    """Primera etiqueta del caso (síntoma u hipótesis) por la que el medicamento está indicado.

    Prioriza síntomas en el orden del caso; si no hay coincidencia, hipótesis en el mismo orden.
    """
    if case.symptoms:
        indicated = set(medication.indicated_symptom_labels)
        for s in case.symptoms:
            if s.label in indicated:
                return s.label
    if case.hypotheses:
        indicated_h = set(medication.indicated_hypothesis_labels)
        for h in case.hypotheses:
            if h.label in indicated_h:
                return h.label
    return None
