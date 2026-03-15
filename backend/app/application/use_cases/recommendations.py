"""Caso de uso de recomendaciones: filtra y ordena medicamentos según el caso clínico."""

from dataclasses import replace

from app.application.ports.medication_repository import MedicationRepository
from app.domain.entities import Medication, StructuredCase
from app.domain.services.recommendation_rules import medication_matches_case

MAX_RECOMMENDATIONS = 5


class RecommendationsUseCase:
    """Obtiene recomendaciones de medicamentos para un caso clínico estructurado."""

    def __init__(
        self,
        *,
        medication_repository: MedicationRepository,
    ) -> None:
        self.medication_repository = medication_repository

    def run(self, case: StructuredCase) -> list[Medication]:
        """Devuelve hasta 5 medicamentos que coinciden con el caso, ordenados por margen (desc); el primero con badge 'main', el resto 'alternative'."""
        candidates = self.medication_repository.get_available()
        matching = [m for m in candidates if medication_matches_case(m, case)]
        sorted_meds = sorted(
            matching,
            key=lambda m: m.economic_margin,
            reverse=True,
        )
        top = sorted_meds[:MAX_RECOMMENDATIONS]
        result: list[Medication] = []
        for i, med in enumerate(top):
            badge = "main" if i == 0 else "alternative"
            result.append(replace(med, badge=badge))
        return result
