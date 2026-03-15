from dataclasses import dataclass
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True)
class Medication:
    """Medicamento del catálogo o recomendación. Usado en catálogo (todos los campos) y en respuesta del motor (badge asignado en el caso de uso: primer resultado main, resto alternative)."""

    id: str
    name: str
    category: str
    reason: str
    badge: Literal["main", "alternative"]
    price: str | None = None
    stock: str | None = None
    format: str | None = None  # noqa: A003
    # Campos para reglas de coincidencia y margen (motor de recomendaciones, video-05)
    age_min: int | None = None
    """Edad mínima indicada; None = sin límite."""
    age_max: int | None = None
    """Edad máxima indicada; None = sin límite."""
    allowed_sexes: tuple[Literal["Hombre", "Mujer"], ...] = ()
    """Sexos para los que está indicado; vacío = cualquiera."""
    suitable_for_pregnancy: bool = False
    """True = apto en embarazo."""
    indicated_symptom_labels: tuple[str, ...] = ()
    """Nombres (labels) de síntomas para los que está indicado. Comparación por nombre."""
    indicated_hypothesis_labels: tuple[str, ...] = ()
    """Nombres (labels) de hipótesis diagnósticas indicadas. Comparación por nombre."""
    economic_margin: Decimal = Decimal("0")
    """Margen económico; mayor = más prioritario al ordenar."""
