"""
Datos de prueba (seed) para el catálogo de medicamentos en modo memoria.

Este catálogo es solo para desarrollo y tests. Con STORAGE_BACKEND=postgresql
(video-07) los medicamentos se cargarán desde la base de datos.

~100 medicamentos para síntomas comunes: dolor de garganta, fiebre, tos, cefalea,
congestión, dolor muscular, acidez, diarrea, estreñimiento, alergia, etc.
"""

from decimal import Decimal

from app.domain.entities import Medication


def _med(
    id: str,
    name: str,
    category: str,
    reason: str,
    price: str,
    stock: str,
    format: str,
    age_min: int | None,
    age_max: int | None,
    symptoms: tuple[str, ...],
    hypotheses: tuple[str, ...],
    economic_margin: str,
    allowed_sexes: tuple = (),
    suitable_for_pregnancy: bool = False,
) -> Medication:
    """Helper para construir Medication con badge por defecto (el caso de uso asigna main/alternative)."""
    return Medication(
        id=id,
        name=name,
        category=category,
        reason=reason,
        badge="main",
        price=price,
        stock=stock,
        format=format,
        age_min=age_min,
        age_max=age_max,
        allowed_sexes=allowed_sexes,
        suitable_for_pregnancy=suitable_for_pregnancy,
        indicated_symptom_labels=symptoms,
        indicated_hypothesis_labels=hypotheses,
        economic_margin=Decimal(economic_margin),
    )


def get_default_medications() -> list[Medication]:
    """Devuelve ~100 medicamentos de ejemplo para síntomas e hipótesis más comunes."""
    return [
        # --- Dolor de garganta / Faringitis (1-15) ---
        _med("med-1", "Paracetamol 500 mg", "Analgésico", "Dolor leve, fiebre", "3.50", "100", "20 comprimidos", 0, 120, ("Dolor de garganta", "Fiebre", "Fiebre leve"), ("Faringitis leve", "Gripe"), "1.20"),
        _med("med-2", "Ibuprofeno 400 mg", "Antiinflamatorio", "Dolor, inflamación", "4.20", "50", "30 comprimidos", 12, 120, ("Dolor de garganta", "Fiebre", "Fiebre leve"), ("Faringitis leve",), "2.00"),
        _med("med-3", "Amoxicilina 500 mg", "Antibiótico", "Infecciones bacterianas", "5.80", "30", "21 cápsulas", 1, 120, ("Dolor de garganta",), ("Faringitis", "Faringitis leve"), "3.50"),
        _med("med-4", "Spray garganta clorhexidina", "Antiséptico local", "Dolor de garganta", "8.50", "40", "30 ml", 6, 120, ("Dolor de garganta",), ("Faringitis leve",), "4.00"),
        _med("med-5", "Caramelos eucalipto y miel", "Demulcente", "Alivio garganta", "2.50", "80", "1 blister", None, None, ("Dolor de garganta",), ("Faringitis leve", "Resfriado común"), "0.50"),
        _med("med-6", "Pastillas garganta benzocaína", "Antiséptico", "Irritación de garganta", "6.00", "35", "24 pastillas", 12, 120, ("Dolor de garganta",), ("Faringitis leve",), "2.20"),
        _med("med-7", "Jarabe própolis garganta", "Natural", "Molestias de garganta", "9.20", "25", "120 ml", 6, 120, ("Dolor de garganta",), ("Faringitis leve", "Resfriado común"), "1.80"),
        _med("med-8", "Spray garganta lidocaína", "Anestésico local", "Dolor intenso garganta", "7.80", "20", "15 ml", 18, 120, ("Dolor de garganta",), ("Faringitis",), "2.50"),
        _med("med-9", "Pastillas isla-moos", "Fitoterapia", "Ronquera, garganta", "5.50", "45", "25 pastillas", 6, 120, ("Dolor de garganta", "Ronquera"), ("Faringitis leve",), "1.40"),
        _med("med-10", "Naproxeno 550 mg", "Antiinflamatorio", "Dolor e inflamación", "4.80", "40", "20 comprimidos", 16, 120, ("Dolor de garganta", "Dolor"), ("Faringitis",), "2.50"),
        _med("med-11", "Paracetamol + vitamina C", "Analgésico", "Dolor y defensas", "6.20", "30", "20 comprimidos", 12, 120, ("Dolor de garganta", "Fiebre"), ("Gripe", "Resfriado común"), "1.90"),
        _med("med-12", "Colutorio clorhexidina", "Antiséptico", "Higiene bucal y garganta", "4.50", "50", "300 ml", 6, 120, ("Dolor de garganta",), (), "1.10"),
        _med("med-13", "Tantum verde spray", "Antiinflamatorio local", "Dolor de garganta", "9.90", "15", "30 ml", 12, 120, ("Dolor de garganta",), ("Faringitis", "Faringitis leve"), "3.20"),
        _med("med-14", "Strepsils miel y limón", "Antiséptico", "Alivio garganta", "6.80", "60", "24 pastillas", 6, 120, ("Dolor de garganta",), ("Faringitis leve", "Resfriado común"), "2.00"),
        _med("med-15", "Angileptol", "Antiséptico", "Infección garganta", "5.20", "28", "20 pastillas", 6, 120, ("Dolor de garganta",), ("Faringitis",), "1.60"),
        # --- Tos (16-28) ---
        _med("med-16", "Jarabe dextrometorfano", "Antitusivo", "Tos seca", "6.20", "25", "120 ml", 6, 120, ("Tos", "Tos seca"), (), "1.80"),
        _med("med-17", "Jarabe codeína", "Antitusivo", "Tos irritativa", "8.50", "20", "120 ml", 18, 120, ("Tos", "Tos seca"), (), "3.00"),
        _med("med-18", "Jarabe ambroxol", "Mucolítico", "Tos con flema", "7.20", "35", "120 ml", 2, 120, ("Tos", "Tos con flema"), ("Bronquitis leve", "Resfriado común"), "2.20"),
        _med("med-19", "Jarabe acetilcisteína", "Mucolítico", "Flemas, tos productiva", "5.80", "40", "200 ml", 2, 120, ("Tos con flema", "Tos"), ("Bronquitis",), "1.70"),
        _med("med-20", "Pastillas tos miel", "Demulcente", "Tos leve", "4.20", "50", "20 pastillas", 6, 120, ("Tos",), ("Resfriado común",), "1.00"),
        _med("med-21", "Jarabe hiedra", "Mucolítico natural", "Tos irritativa", "6.90", "30", "100 ml", 0, 120, ("Tos", "Tos con flema"), ("Bronquitis leve",), "2.10"),
        _med("med-22", "Iniston tos", "Antitusivo", "Tos seca nocturna", "7.50", "18", "120 ml", 6, 120, ("Tos", "Tos seca"), (), "2.40"),
        _med("med-23", "Bisolvon junior", "Mucolítico", "Tos con mocos", "5.50", "25", "100 ml", 2, 12, ("Tos", "Tos con flema", "Congestión nasal"), ("Resfriado común",), "1.50"),
        _med("med-24", "Pulmo bael tos", "Fitoterapia", "Tos y garganta", "8.20", "22", "150 ml", 6, 120, ("Tos", "Dolor de garganta"), ("Resfriado común", "Faringitis leve"), "2.30"),
        _med("med-25", "Tussiflex", "Antitusivo", "Tos seca", "6.40", "30", "120 ml", 12, 120, ("Tos seca", "Tos"), (), "1.90"),
        _med("med-26", "Fluimucil 600", "Mucolítico", "Flemas espesas", "4.90", "20", "20 sobres", 14, 120, ("Tos con flema",), ("Bronquitis",), "1.40"),
        _med("med-27", "Jarabe tomillo", "Natural", "Tos y resfriado", "3.80", "45", "120 ml", 3, 120, ("Tos", "Congestión nasal"), ("Resfriado común",), "0.90"),
        _med("med-28", "Mucosan tos", "Mucolítico", "Tos productiva", "5.20", "28", "120 ml", 2, 120, ("Tos con flema", "Tos"), (), "1.30"),
        # --- Fiebre / Gripe / Resfriado (29-42) ---
        _med("med-29", "Paracetamol 1 g", "Antitérmico", "Fiebre y dolor", "4.00", "30", "20 comprimidos", 12, 120, ("Fiebre", "Dolor"), ("Gripe", "Resfriado común"), "1.50"),
        _med("med-30", "Apiretal 100 mg/ml", "Antitérmico", "Fiebre niños", "5.20", "40", "90 ml", 0, 12, ("Fiebre",), ("Gripe", "Resfriado común"), "1.80"),
        _med("med-31", "Frenadol", "Antigripal", "Gripe, fiebre, congestión", "6.50", "35", "10 sobres", 15, 120, ("Fiebre", "Congestión nasal", "Dolor"), ("Gripe", "Resfriado común"), "2.50"),
        _med("med-32", "Couldina", "Antigripal", "Síntomas gripales", "5.80", "28", "10 cápsulas", 12, 120, ("Fiebre", "Tos", "Congestión nasal"), ("Gripe",), "2.20"),
        _med("med-33", "Vitamina C 1 g", "Suplemento", "Defensas, resfriado", "7.00", "60", "20 comprimidos", 14, 120, ("Fiebre",), (), "0.90", suitable_for_pregnancy=True),
        _med("med-34", "Aspirina 500 mg", "Antitérmico", "Fiebre, dolor", "3.20", "40", "20 comprimidos", 16, 120, ("Fiebre", "Dolor", "Dolor de cabeza"), ("Gripe",), "1.10"),
        _med("med-35", "Efferalgan 500", "Paracetamol", "Fiebre y dolor leve", "4.50", "16", "16 comprimidos", 6, 120, ("Fiebre", "Dolor"), ("Resfriado común", "Gripe"), "1.60"),
        _med("med-36", "Antigripal cinfa", "Sintomático", "Gripe", "4.20", "20", "10 sobres", 18, 120, ("Fiebre", "Congestión nasal", "Tos"), ("Gripe", "Resfriado común"), "1.30"),
        _med("med-37", "Iniston gripe", "Antigripal", "Síntomas gripe", "7.20", "12", "12 cápsulas", 18, 65, ("Fiebre", "Dolor muscular", "Congestión nasal"), ("Gripe",), "2.80"),
        _med("med-38", "Propolis defensas", "Natural", "Resfriado y defensas", "12.50", "25", "30 ml", 6, 120, ("Fiebre", "Congestión nasal"), ("Resfriado común",), "3.20"),
        _med("med-39", "Paracetamol pediátrico", "Antitérmico", "Fiebre niños", "4.00", "15", "120 ml", 0, 12, ("Fiebre",), (), "1.50"),
        _med("med-40", "Echinacea complex", "Fitoterapia", "Prevención resfriado", "9.80", "30", "60 cápsulas", 12, 120, (), ("Resfriado común",), "2.40"),
        _med("med-41", "Complejo B inyectable", "Suplemento", "Cansancio, defensas", "12.00", "0", "5 ampollas", 18, 120, ("Fiebre", "Cansancio"), (), "5.00"),
        _med("med-42", "Redoxon vitamina C", "Suplemento", "Resfriado", "8.50", "45", "20 comprimidos", 12, 120, ("Fiebre", "Cansancio"), ("Resfriado común",), "2.00"),
        # --- Dolor de cabeza / Cefalea (43-54) ---
        _med("med-43", "Ibuprofeno 600 mg", "Analgésico", "Dolor de cabeza intenso", "5.20", "30", "20 comprimidos", 12, 120, ("Dolor de cabeza", "Dolor"), ("Cefalea tensional", "Migraña"), "2.20"),
        _med("med-44", "Nolotil", "Analgésico", "Dolor intenso", "6.80", "20", "20 cápsulas", 18, 120, ("Dolor de cabeza", "Dolor"), ("Cefalea", "Migraña"), "2.80"),
        _med("med-45", "Enantyum 25 mg", "Antiinflamatorio", "Dolor agudo", "4.50", "20", "20 comprimidos", 18, 120, ("Dolor de cabeza", "Dolor muscular"), ("Cefalea tensional",), "1.90"),
        _med("med-46", "Aspirina 100 mg", "Antiagregante", "Prevención cardiovascular", "2.80", "30", "30 comprimidos", 18, 120, (), (), "0.50"),
        _med("med-47", "Paracetamol 650 mg", "Analgésico", "Cefalea leve", "3.80", "24", "24 comprimidos", 6, 120, ("Dolor de cabeza",), ("Cefalea tensional",), "1.20"),
        _med("med-48", "Migraña stop", "Analgésico", "Migraña", "7.50", "12", "12 comprimidos", 18, 120, ("Dolor de cabeza",), ("Migraña",), "3.50"),
        _med("med-49", "Sumial 50 mg", "Betabloqueante", "Prevención migraña", "3.20", "28", "28 comprimidos", 18, 120, (), ("Migraña",), "0.80"),
        _med("med-50", "Dolgit", "Ibuprofeno", "Dolor y fiebre", "4.20", "40", "30 comprimidos", 12, 120, ("Dolor de cabeza", "Fiebre"), ("Cefalea tensional", "Gripe"), "1.60"),
        _med("med-51", "Cafiaspirina", "Analgésico", "Dolor de cabeza", "3.50", "20", "20 comprimidos", 16, 120, ("Dolor de cabeza",), ("Cefalea tensional",), "1.10"),
        _med("med-52", "Buscapina compositum", "Antiespasmódico", "Dolor abdominal y cefalea", "6.20", "20", "20 comprimidos", 18, 120, ("Dolor de cabeza", "Dolor abdominal"), ("Cólico",), "2.00"),
        _med("med-53", "Gelocatil 650", "Paracetamol", "Dolor leve a moderado", "4.80", "30", "30 comprimidos", 6, 120, ("Dolor de cabeza", "Dolor"), ("Cefalea tensional",), "1.40"),
        _med("med-54", "Actron 400", "Ibuprofeno", "Dolor e inflamación", "3.90", "25", "25 comprimidos", 12, 120, ("Dolor de cabeza", "Dolor muscular"), ("Cefalea",), "1.30"),
        # --- Congestión nasal / Rinitis (55-64) ---
        _med("med-55", "Frenadol descongestivo", "Descongestivo", "Congestión nasal", "6.80", "15", "10 sobres", 15, 120, ("Congestión nasal", "Mocos"), ("Resfriado común", "Rinitis"), "2.40"),
        _med("med-56", "Aspirina complex", "Analgésico descongestivo", "Resfriado con congestión", "7.20", "20", "20 comprimidos", 16, 120, ("Congestión nasal", "Fiebre", "Dolor"), ("Resfriado común",), "2.60"),
        _med("med-57", "Rino Ebastel", "Antihistamínico", "Rinitis alérgica", "8.50", "30", "30 comprimidos", 12, 120, ("Congestión nasal", "Estornudos", "Picor nasal"), ("Rinitis alérgica",), "2.90"),
        _med("med-58", "Aerius 5 mg", "Antihistamínico", "Alergia, rinitis", "6.50", "30", "30 comprimidos", 12, 120, ("Congestión nasal", "Estornudos", "Picor"), ("Rinitis alérgica", "Alergia"), "2.20"),
        _med("med-59", "Spray nasal pseudoefedrina", "Descongestivo", "Congestión nasal", "5.20", "25", "15 ml", 12, 120, ("Congestión nasal",), ("Resfriado común", "Rinitis"), "1.70"),
        _med("med-60", "María natura spray nasal", "Natural", "Congestión leve", "7.80", "20", "20 ml", 6, 120, ("Congestión nasal",), ("Resfriado común",), "2.10"),
        _med("med-61", "Bisolvon nasal", "Descongestivo", "Mocos y congestión", "4.50", "30", "15 ml", 6, 120, ("Congestión nasal", "Mocos"), ("Resfriado común",), "1.30"),
        _med("med-62", "Reactine", "Antihistamínico", "Rinitis y urticaria", "9.20", "14", "14 comprimidos", 12, 120, ("Congestión nasal", "Estornudos", "Picor"), ("Rinitis alérgica",), "3.00"),
        _med("med-63", "Clarityne", "Antihistamínico", "Alergia estacional", "5.80", "30", "30 comprimidos", 2, 120, ("Congestión nasal", "Estornudos"), ("Rinitis alérgica",), "1.80"),
        _med("med-64", "Agua de mar spray", "Higiene nasal", "Lavado nasal", "4.20", "50", "100 ml", 0, 120, ("Congestión nasal", "Mocos"), ("Resfriado común", "Rinitis"), "0.90"),
        # --- Dolor muscular / Contracturas (65-72) ---
        _med("med-65", "Dolgit gel", "Antiinflamatorio tópico", "Dolor muscular", "8.50", "35", "100 g", 12, 120, ("Dolor muscular", "Dolor"), ("Contractura muscular", "Lumbalgia"), "2.80"),
        _med("med-66", "Voltaren 1% gel", "Diclofenaco tópico", "Dolor e inflamación local", "9.20", "40", "100 g", 14, 120, ("Dolor muscular", "Dolor articular"), ("Contractura muscular", "Lumbalgia"), "3.20"),
        _med("med-67", "Flector 1%", "Ketoprofeno tópico", "Dolor muscular", "10.50", "25", "50 g", 15, 120, ("Dolor muscular",), ("Contractura muscular", "Esguince leve"), "3.50"),
        _med("med-68", "Ibuprofeno gel", "Antiinflamatorio tópico", "Dolor local", "6.80", "45", "60 g", 12, 120, ("Dolor muscular",), ("Contractura muscular",), "2.00"),
        _med("med-69", "Reflex spray", "Analgésico tópico", "Dolor muscular y articular", "7.50", "30", "100 ml", 12, 120, ("Dolor muscular", "Dolor"), ("Lumbalgia", "Contractura muscular"), "2.40"),
        _med("med-70", "Musculare 400", "Relajante muscular", "Contracturas", "5.20", "20", "20 comprimidos", 18, 120, ("Dolor muscular",), ("Contractura muscular", "Lumbalgia"), "1.90"),
        _med("med-71", "Mioflex crema", "Relajante tópico", "Tensión muscular", "8.20", "28", "50 g", 18, 120, ("Dolor muscular",), ("Contractura muscular",), "2.60"),
        _med("med-72", "Calor gel", "Rubefaciente", "Dolor muscular leve", "4.50", "40", "75 g", 12, 120, ("Dolor muscular",), (), "1.20"),
        # --- Acidez / Reflujo / Estómago (73-82) ---
        _med("med-73", "Omeprazol 20 mg", "Inhibidor bomba protones", "Acidez, reflujo", "3.50", "28", "28 cápsulas", 18, 120, ("Acidez", "Ardor de estómago"), ("Reflujo gastroesofágico",), "1.00"),
        _med("med-74", "Almax", "Antiácido", "Acidez puntual", "5.20", "24", "24 comprimidos", 12, 120, ("Acidez", "Ardor de estómago"), (), "1.80"),
        _med("med-75", "Gaviscon", "Antiácido", "Acidez y reflujo", "6.80", "24", "24 comprimidos", 12, 120, ("Acidez", "Ardor de estómago"), ("Reflujo gastroesofágico",), "2.20"),
        _med("med-76", "Ranitidina 150 mg", "Antagonista H2", "Acidez", "2.80", "20", "20 comprimidos", 12, 120, ("Acidez",), ("Reflujo",), "0.70"),
        _med("med-77", "Bicarbonato sódico", "Antiácido", "Acidez leve", "1.50", "60", "100 comprimidos", 12, 120, ("Acidez",), (), "0.30"),
        _med("med-78", "Nexium 20 mg", "IBP", "Reflujo y acidez", "8.50", "28", "28 comprimidos", 18, 120, ("Acidez", "Ardor de estómago"), ("Reflujo gastroesofágico",), "3.00"),
        _med("med-79", "Urbason 4 mg", "Corticoides", "Alergia grave", "4.20", "30", "30 comprimidos", 6, 120, (), ("Alergia",), "1.20"),
        _med("med-80", "Motilium", "Procinético", "Náuseas, digestiones lentas", "6.20", "30", "30 comprimidos", 12, 120, ("Náuseas", "Dolor abdominal"), (), "2.00"),
        _med("med-81", "Primperan", "Antiemético", "Náuseas y vómitos", "3.80", "30", "30 comprimidos", 1, 120, ("Náuseas",), (), "1.10"),
        _med("med-82", "Biodramina", "Antiemético", "Mareo y náuseas", "7.50", "10", "10 comprimidos", 2, 120, ("Náuseas", "Mareo"), (), "2.50"),
        # --- Diarrea / Estreñimiento (83-92) ---
        _med("med-83", "Fortasec", "Antidiarreico", "Diarrea aguda", "6.50", "12", "12 cápsulas", 12, 120, ("Diarrea",), ("Gastroenteritis",), "2.40"),
        _med("med-84", "Smecta", "Adsorbente", "Diarrea", "5.80", "30", "30 sobres", 0, 120, ("Diarrea", "Dolor abdominal"), ("Gastroenteritis",), "1.90"),
        _med("med-85", "Ultra levura", "Probiótico", "Diarrea y flora intestinal", "8.20", "20", "20 cápsulas", 2, 120, ("Diarrea",), ("Gastroenteritis",), "2.60"),
        _med("med-86", "Floratil", "Probiótico", "Diarrea asociada a antibióticos", "9.50", "10", "10 cápsulas", 0, 120, ("Diarrea",), (), "3.00"),
        _med("med-87", "Dulcolaxo", "Laxante", "Estreñimiento", "4.20", "20", "20 comprimidos", 12, 120, ("Estreñimiento",), (), "1.30"),
        _med("med-88", "Plantaben", "Laxante fibra", "Estreñimiento ocasional", "6.80", "30", "30 sobres", 12, 120, ("Estreñimiento",), (), "2.00"),
        _med("med-89", "Puntual", "Laxante", "Estreñimiento", "3.50", "28", "28 comprimidos", 18, 120, ("Estreñimiento",), (), "1.00"),
        _med("med-90", "Lactulosa", "Laxante osmótico", "Estreñimiento", "5.20", "20", "300 ml", 0, 120, ("Estreñimiento",), (), "1.50"),
        _med("med-91", "Enterogermina", "Probiótico", "Diarrea y equilibrio intestinal", "12.50", "20", "20 viales", 0, 120, ("Diarrea",), ("Gastroenteritis",), "3.50"),
        _med("med-92", "Carbonato activado", "Adsorbente", "Diarrea e intoxicación leve", "4.00", "40", "30 cápsulas", 12, 120, ("Diarrea",), (), "1.20"),
        # --- Alergia / Picor / Piel (93-100) ---
        _med("med-93", "Ebastel 10 mg", "Antihistamínico", "Alergia, urticaria", "5.50", "30", "30 comprimidos", 12, 120, ("Picor", "Estornudos", "Congestión nasal"), ("Rinitis alérgica", "Alergia"), "1.80"),
        _med("med-94", "Polaramine", "Antihistamínico", "Alergia y picor", "6.20", "20", "20 comprimidos", 2, 120, ("Picor", "Urticaria"), ("Alergia", "Dermatitis"), "2.00"),
        _med("med-95", "Atarax 25 mg", "Antihistamínico", "Picor y ansiedad leve", "4.80", "30", "30 comprimidos", 6, 120, ("Picor", "Ansiedad"), ("Alergia", "Dermatitis"), "1.50"),
        _med("med-96", "Cortisona crema 1%", "Corticoide tópico", "Picor e inflamación piel", "3.20", "30", "30 g", 2, 120, ("Picor", "Dermatitis"), ("Dermatitis", "Eczema"), "1.00"),
        _med("med-97", "Fenistil gel", "Antihistamínico tópico", "Picor y picaduras", "7.50", "30", "30 g", 0, 120, ("Picor",), ("Picadura", "Alergia cutánea"), "2.40"),
        _med("med-98", "After bite", "Picaduras", "Picor por picadura", "5.80", "25", "10 ml", 0, 120, ("Picor",), ("Picadura",), "1.60"),
        _med("med-99", "Caladryl", "Antipruriginoso", "Picor y quemaduras solares", "6.50", "22", "100 ml", 2, 120, ("Picor",), ("Quemadura solar", "Dermatitis"), "2.10"),
        _med("med-100", "Bepanthol crema", "Emoliente", "Piel seca e irritada", "7.20", "35", "50 g", 0, 120, ("Picor", "Piel seca"), ("Dermatitis",), "2.20"),
    ]