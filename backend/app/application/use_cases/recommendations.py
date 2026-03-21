"""Caso de uso de recomendaciones: agrupa por síntoma (3 productos/síntoma) ordenados por margen."""

from dataclasses import dataclass, replace

from app.application.ports.medication_repository import MedicationRepository
from app.domain.entities import Medication, StructuredCase
from app.domain.services.recommendation_rules import medication_matches_case

PRODUCTS_PER_SYMPTOM = 3


@dataclass(frozen=True)
class SymptomRecommendationGroupResult:
    """Grupo de recomendaciones asociado a un síntoma del caso (o sin agrupar si no hay síntomas)."""

    symptom_label: str | None
    medications: tuple[Medication, ...]


class RecommendationsUseCase:
    """Obtiene recomendaciones de medicamentos para un caso clínico estructurado."""

    def __init__(
        self,
        *,
        medication_repository: MedicationRepository,
    ) -> None:
        self.medication_repository = medication_repository

    def _top_medications_for_symptom(
        self,
        candidates: list[Medication],
        case: StructuredCase,
        symptom_label: str,
    ) -> tuple[Medication, ...]:
        matching = [
            m
            for m in candidates
            if medication_matches_case(m, case)
            and symptom_label in m.indicated_symptom_labels
        ]
        sorted_meds = sorted(
            matching,
            key=lambda m: m.economic_margin,
            reverse=True,
        )
        top = sorted_meds[:PRODUCTS_PER_SYMPTOM]
        return tuple(self._with_badges(top))

    @staticmethod
    def _with_badges(medications: list[Medication]) -> list[Medication]:
        out: list[Medication] = []
        for i, med in enumerate(medications):
            badge = "main" if i == 0 else "alternative"
            out.append(replace(med, badge=badge))
        return out

    async def run(self, case: StructuredCase) -> list[SymptomRecommendationGroupResult]:
        """Por cada síntoma del caso: hasta 3 medicamentos que lo indican y cumplen el caso, por margen desc.

        Sin síntomas en el caso: una sola lista global (máx. 3), ordenada por margen.
        """
        candidates = await self.medication_repository.get_available()
        if case.symptoms:
            return [
                SymptomRecommendationGroupResult(
                    symptom_label=s.label,
                    medications=self._top_medications_for_symptom(
                        candidates, case, s.label
                    ),
                )
                for s in case.symptoms
            ]

        matching = [m for m in candidates if medication_matches_case(m, case)]
        sorted_meds = sorted(
            matching,
            key=lambda m: m.economic_margin,
            reverse=True,
        )
        top = sorted_meds[:PRODUCTS_PER_SYMPTOM]
        meds = tuple(
            replace(m, badge="main" if i == 0 else "alternative")
            for i, m in enumerate(top)
        )
        return [SymptomRecommendationGroupResult(symptom_label=None, medications=meds)]
