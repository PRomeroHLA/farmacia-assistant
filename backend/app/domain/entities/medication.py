from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Medication:
    """Medicamento del catálogo o recomendación. El motor de recomendaciones trabaja con Medication; la API lo expone como ProductRecommendation (mismos campos)."""

    id: str
    name: str
    category: str
    reason: str
    badge: Literal["main", "alternative"]
    price: str | None = None
    stock: str | None = None
    format: str | None = None  # noqa: A003
