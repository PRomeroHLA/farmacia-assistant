"""Schemas Pydantic para recomendaciones. Coinciden con frontend ProductRecommendation (recommendations.ts)."""

from typing import Literal

from pydantic import BaseModel


class ProductRecommendation(BaseModel):
    """Recomendación de producto. Mismos campos que frontend ProductRecommendation."""

    id: str
    name: str
    category: str
    reason: str
    badge: Literal["main", "alternative"]
    price: str | None = None
    stock: str | None = None
    format: str | None = None  # noqa: A003
