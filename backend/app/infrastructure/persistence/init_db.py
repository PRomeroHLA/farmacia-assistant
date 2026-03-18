"""Inicialización y seed de la base de datos (PostgreSQL async).

Ejecutar:
  cd backend
  python -m app.infrastructure.persistence.init_db
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select

from app.infrastructure.config import Settings, get_settings
from app.infrastructure.persistence.memory.seed_medications import get_default_medications
from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.models.engine import (
    get_async_engine,
    get_async_session_maker,
)
from app.infrastructure.persistence.models.medication import (
    MedicationModel,
    MedicationStockModel,
)
from app.infrastructure.persistence.models.user import UserModel
from app.infrastructure.security.password import hash_password


def _get_meds_to_seed(settings: Settings) -> list:
    """Devuelve los medicamentos a sembrar según configuración.

    Por defecto (MEDS_SEED_LIMIT=None) carga todos los medicamentos del seed.
    """
    meds = get_default_medications()
    limit = getattr(settings, "MEDS_SEED_LIMIT", None)
    if limit is None:
        return meds
    try:
        limit_int = int(limit)
    except (TypeError, ValueError):
        return meds
    if limit_int <= 0:
        return []
    return meds[:limit_int]


def _join_csv(values: tuple[str, ...]) -> str:
    return ",".join(v.strip() for v in values if v and v.strip())


def _parse_quantity(stock: str | None) -> int:
    if stock is None:
        return 0
    s = str(stock).strip()
    if s == "":
        return 0
    try:
        return int(s)
    except ValueError:
        # Si viene un label tipo "En stock", asumimos >0
        lowered = s.lower()
        if "sin" in lowered and "stock" in lowered:
            return 0
        return 10


async def init_db(settings: Settings) -> None:
    """Crea las tablas a partir de Base.metadata."""
    if settings.DATABASE_URL is None or settings.DATABASE_URL.strip() == "":
        raise ValueError("DATABASE_URL es obligatoria para init_db()")
    engine = get_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def seed_db(settings: Settings) -> None:
    """Inserta datos de ejemplo (idempotente): usuario de prueba + algunos medicamentos y stock."""
    if settings.DATABASE_URL is None or settings.DATABASE_URL.strip() == "":
        raise ValueError("DATABASE_URL es obligatoria para seed_db()")

    engine = get_async_engine(settings.DATABASE_URL)
    session_maker = get_async_session_maker(engine)

    async with session_maker() as session:
        async with session.begin():
            # --- Usuario de prueba ---
            username = "pharmacist"
            existing_user = await session.execute(
                select(UserModel).where(UserModel.username == username).limit(1)
            )
            if existing_user.scalar_one_or_none() is None:
                session.add(
                    UserModel(
                        id="pharmacist-1",
                        username=username,
                        full_name="Farmacéutico/a de prueba",
                        password_hash=hash_password("pharmacist123"),
                    )
                )

            # --- Medicamentos + stock (seed desde catálogo en memoria) ---
            meds = _get_meds_to_seed(settings)
            for m in meds:
                existing_med = await session.execute(
                    select(MedicationModel).where(MedicationModel.id == m.id).limit(1)
                )
                if existing_med.scalar_one_or_none() is None:
                    session.add(
                        MedicationModel(
                            id=m.id,
                            name=m.name,
                            category=m.category,
                            reason=m.reason,
                            price=m.price,
                            format=m.format,
                            age_min=m.age_min,
                            age_max=m.age_max,
                            allowed_sexes=_join_csv(m.allowed_sexes),
                            suitable_for_pregnancy=bool(m.suitable_for_pregnancy),
                            indicated_symptom_labels=_join_csv(m.indicated_symptom_labels),
                            indicated_hypothesis_labels=_join_csv(m.indicated_hypothesis_labels),
                            economic_margin=m.economic_margin,
                        )
                    )

                # stock row (idempotente por medication_id)
                existing_stock = await session.execute(
                    select(MedicationStockModel)
                    .where(MedicationStockModel.medication_id == m.id)
                    .limit(1)
                )
                if existing_stock.scalar_one_or_none() is None:
                    session.add(
                        MedicationStockModel(
                            medication_id=m.id,
                            quantity=_parse_quantity(m.stock),
                        )
                    )

    await engine.dispose()


async def _main() -> None:
    settings = get_settings()
    if settings.STORAGE_BACKEND != "postgresql":
        raise RuntimeError(
            'Para inicializar la BD, configura STORAGE_BACKEND="postgresql" y DATABASE_URL.'
        )
    await init_db(settings)
    await seed_db(settings)


if __name__ == "__main__":
    asyncio.run(_main())

