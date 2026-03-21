"""Repositorio de medicamentos sobre PostgreSQL (SQLAlchemy async)."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.ports import MedicationRepository
from app.domain.entities import Medication
from app.infrastructure.persistence.models import MedicationModel, MedicationStockModel


def _split_csv(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    parts = [p.strip() for p in value.split(",")]
    return tuple(p for p in parts if p)


def _stock_label(quantity: int | None) -> str | None:
    if quantity is None:
        return None
    if quantity <= 0:
        return "Sin stock"
    if quantity <= 5:
        return "Pocas unidades"
    return "En stock"


def _row_to_medication(model: MedicationModel, quantity: int | None) -> Medication:
    margin = model.economic_margin
    economic_margin = margin if isinstance(margin, Decimal) else Decimal(str(margin))

    return Medication(
        id=model.id,
        name=model.name,
        category=model.category,
        reason=model.reason,
        badge="alternative",  # El caso de uso asigna main/alternative en la salida
        price=model.price,
        stock=_stock_label(quantity),
        stock_quantity=quantity,
        format=model.format,
        age_min=model.age_min,
        age_max=model.age_max,
        allowed_sexes=tuple(_split_csv(model.allowed_sexes)),  # type: ignore[arg-type]
        suitable_for_pregnancy=bool(model.suitable_for_pregnancy),
        indicated_symptom_labels=_split_csv(model.indicated_symptom_labels),
        indicated_hypothesis_labels=_split_csv(model.indicated_hypothesis_labels),
        economic_margin=economic_margin,
    )


class PostgresMedicationRepository(MedicationRepository):
    """Implementación de MedicationRepository con PostgreSQL. Usa un sessionmaker async inyectado."""

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def get_all(self) -> list[Medication]:
        stmt = select(MedicationModel, MedicationStockModel.quantity).outerjoin(
            MedicationStockModel, MedicationStockModel.medication_id == MedicationModel.id
        )
        async with self._session_maker() as session:
            result = await session.execute(stmt)
            rows = result.all()
            return [_row_to_medication(m, q) for (m, q) in rows]

    async def get_by_id(self, id: str) -> Medication | None:
        stmt = (
            select(MedicationModel, MedicationStockModel.quantity)
            .outerjoin(
                MedicationStockModel, MedicationStockModel.medication_id == MedicationModel.id
            )
            .where(MedicationModel.id == id)
            .limit(1)
        )
        async with self._session_maker() as session:
            result = await session.execute(stmt)
            row = result.first()
            if row is None:
                return None
            model, qty = row
            return _row_to_medication(model, qty)

    async def get_available(self) -> list[Medication]:
        stmt = (
            select(MedicationModel, MedicationStockModel.quantity)
            .join(MedicationStockModel, MedicationStockModel.medication_id == MedicationModel.id)
            .where(MedicationStockModel.quantity > 0)
        )
        async with self._session_maker() as session:
            result = await session.execute(stmt)
            rows = result.all()
            return [_row_to_medication(m, q) for (m, q) in rows]

