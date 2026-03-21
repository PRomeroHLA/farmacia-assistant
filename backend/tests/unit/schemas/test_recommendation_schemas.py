"""Tests de contrato para schemas de recomendaciones. Alineados con frontend recommendations.ts."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.domain.entities import ClinicalHypothesis, Medication, StructuredCase, Symptom
from app.interfaces.api.schemas.recommendation import (
    ProductRecommendation,
    medication_to_product_recommendation,
)


def test_product_recommendation_has_required_fields():
    """ProductRecommendation: id, name, category, reason, badge (main|alternative)."""
    p = ProductRecommendation(
        id="med-1",
        name="Paracetamol 500 mg",
        category="Analgésico",
        reason="Dolor leve",
        badge="main",
    )
    data = p.model_dump(by_alias=True)
    assert data["id"] == "med-1"
    assert data["name"] == "Paracetamol 500 mg"
    assert data["category"] == "Analgésico"
    assert data["reason"] == "Dolor leve"
    assert data["badge"] == "main"


def test_product_recommendation_optional_fields():
    """ProductRecommendation: price, stock, format opcionales."""
    p = ProductRecommendation(
        id="med-2",
        name="Ibuprofeno",
        category="Antiinflamatorio",
        reason="Inflamación",
        badge="alternative",
        price="4.20",
        stock="50",
        format="30 comprimidos",
    )
    data = p.model_dump(by_alias=True)
    assert data.get("price") == "4.20"
    assert data.get("stock") == "50"
    assert data.get("format") == "30 comprimidos"


def test_product_recommendation_badge_only_main_or_alternative():
    """badge solo acepta 'main' o 'alternative'."""
    for badge in ("main", "alternative"):
        p = ProductRecommendation(
            id="x", name="X", category="Y", reason="Z", badge=badge,
        )
        assert p.model_dump(by_alias=True)["badge"] == badge

    with pytest.raises(ValidationError):
        ProductRecommendation(
            id="x", name="X", category="Y", reason="Z", badge="invalid",
        )


def test_medication_to_product_recommendation_sets_stock_margin_and_match_label():
    case = StructuredCase(
        age=40,
        sex="Mujer",
        is_pregnant=False,
        symptoms=[Symptom(id="s1", label="Congestión nasal")],
        hypotheses=[ClinicalHypothesis(id="h1", label="Resfriado común")],
    )
    med = Medication(
        id="med-x",
        name="Inhalador",
        category="Dispositivo",
        reason="Alivio nasal",
        badge="main",
        price="18.90€",
        stock="8",
        format="1 unidad",
        indicated_symptom_labels=("Congestión nasal", "Rinorrea"),
        indicated_hypothesis_labels=("Resfriado común",),
        economic_margin=Decimal("6.50"),
    )
    dto = medication_to_product_recommendation(med, case)
    assert dto.recommended_for == "Congestión nasal"
    assert dto.commercial_margin == "6,50 €"
    assert dto.stock == "En stock"
    assert dto.stock_units == "8"
    dumped = dto.model_dump(mode="json", by_alias=True)
    assert dumped["recommendedFor"] == "Congestión nasal"
    assert dumped["commercialMargin"] == "6,50 €"
    assert dumped["stockUnits"] == "8"


def test_medication_to_product_recommendation_respects_recommended_for_override():
    case = StructuredCase(
        age=40,
        sex="Mujer",
        is_pregnant=False,
        symptoms=[Symptom(id="s1", label="Tos")],
        hypotheses=[],
    )
    med = Medication(
        id="med-x",
        name="X",
        category="C",
        reason="R",
        badge="main",
        indicated_symptom_labels=("Tos",),
        economic_margin=Decimal("1"),
    )
    dto = medication_to_product_recommendation(
        med, case, recommended_for_override="Tos"
    )
    assert dto.recommended_for == "Tos"
