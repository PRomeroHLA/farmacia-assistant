"""Extractor de estructura clínica usando LangChain y OpenAI. Requiere OPENAI_API_KEY cuando LLM_EXTRACTOR=openai."""

import json
import re
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from functools import lru_cache

from app.application.ports.case_structure_extractor import CaseStructureExtractor
from app.domain.entities import ClinicalHypothesis, StructuredCase, Symptom


def _format_catalog_list(values: tuple[str, ...]) -> str:
    """Muestra una lista con un elemento por línea para facilitar que el LLM elija."""
    return "\n".join(f"- {v}" for v in values)


@lru_cache(maxsize=1)
def _get_vocabulary() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Carga vocabulario canónico desde el archivo curado."""
    vocab_file = (
        Path(__file__).resolve().parents[1]
        / "persistence"
        / "memory"
        / "diagnosticos_y_sintomas_comunes.txt"
    )

    try:
        raw = vocab_file.read_text(encoding="utf-8")
    except OSError:
        return (), ()

    diagnoses: list[str] = []
    symptoms: list[str] = []
    section: str | None = None

    # Matches "01. Label", "001. Label", etc.
    num_dot_re = re.compile(r"^\s*(\d{1,3})\.\s*(.+?)\s*$")

    for line in raw.splitlines():
        if not line.strip():
            continue
        lower = line.lower()
        if "diagnósticos comunes" in lower:
            section = "diagnoses"
            continue
        if "síntomas comunes" in lower:
            section = "symptoms"
            continue

        m = num_dot_re.match(line)
        if not m or not section:
            continue

        label = m.group(2).strip()
        if not label:
            continue

        if section == "diagnoses":
            diagnoses.append(label)
        elif section == "symptoms":
            symptoms.append(label)

    return tuple(symptoms), tuple(diagnoses)


def _build_extract_prompt(case_text: str) -> str:
    """Construye el prompt forzando clasificación contra el catálogo canónico."""
    symptoms, diagnoses = _get_vocabulary()
    catalog_symptoms = _format_catalog_list(symptoms)
    catalog_diagnoses = _format_catalog_list(diagnoses)

    return f"""Analiza el siguiente texto de un caso clínico y extrae la información estructurada.

TEXTO DEL CASO:
---
{case_text.strip() or "(sin texto)"}
---

CATALOGO CANONICO (obligatorio para normalizar etiquetas):
SINTOMAS (elige SOLO etiquetas exactas):
{catalog_symptoms}

DIAGNOSTICOS (elige SOLO etiquetas exactas):
{catalog_diagnoses}

Reglas de clasificación:
1) Para "symptoms", devuelve únicamente etiquetas que aparezcan en el catálogo de SINTOMAS.
2) Para "hypotheses", devuelve únicamente etiquetas que aparezcan en el catálogo de DIAGNOSTICOS.
3) Usa las etiquetas con el mismo texto exacto (mayúsculas, acentos, paréntesis, guiones y sufijos como "COVID-19").
4) Si un término del texto NO coincide claramente con el catálogo, usa el mejor match, pero sin inventar etiquetas fuera del catálogo.
5) Deduplica etiquetas: si el mismo síntoma aparece varias veces, devuelve una sola vez.

Devuelve ÚNICAMENTE un objeto JSON válido (sin markdown ni texto adicional) con exactamente estos campos:
- "age": número entero (años) o null si no se menciona o no está claro
- "sex": "Hombre" o "Mujer" o null si no se indica
- "is_pregnant": true solo si se menciona embarazo explícitamente; false en caso contrario
- "symptoms": lista de strings con las etiquetas canónicas de síntomas detectados. Lista vacía [] si no hay ninguno
- "hypotheses": lista de strings con las hipótesis diagnósticas sugeridas. Dedúcelas de los síntomas si es posible. Lista vacía [] si no hay ninguna
Si no hay información clara para un campo, usa null para age/sex o lista vacía para symptoms/hypotheses. No inventes datos."""


class CaseStructureExtractionError(Exception):
    """Error al extraer la estructura del caso (respuesta no JSON válido o formato incorrecto)."""

    pass


def _parse_json_from_response(content: str) -> dict:
    """Extrae y parsea JSON del contenido de la respuesta. Acepta texto envuelto en ```json ... ```."""
    text = content.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise CaseStructureExtractionError(f"La respuesta del modelo no es JSON válido: {e}") from e


def _map_json_to_structured_case(data: dict) -> StructuredCase:
    """Mapea el diccionario parseado a la entidad StructuredCase. Asigna ids sym-1, hyp-1, etc."""
    age = data.get("age")
    if age is not None and not isinstance(age, int):
        try:
            age = int(age)
        except (TypeError, ValueError):
            age = None

    sex = data.get("sex")
    if sex not in ("Hombre", "Mujer"):
        sex = None

    is_pregnant = bool(data.get("is_pregnant") is True)

    symptoms_raw = data.get("symptoms")
    if not isinstance(symptoms_raw, list):
        symptoms_raw = []
    symptoms = [
        Symptom(id=f"sym-{i+1}", label=str(s).strip())
        for i, s in enumerate(symptoms_raw)
        if s and str(s).strip()
    ]

    hypotheses_raw = data.get("hypotheses")
    if not isinstance(hypotheses_raw, list):
        hypotheses_raw = []
    hypotheses = [
        ClinicalHypothesis(id=f"hyp-{i+1}", label=str(h).strip())
        for i, h in enumerate(hypotheses_raw)
        if h and str(h).strip()
    ]

    return StructuredCase(
        age=age,
        sex=sex,
        is_pregnant=is_pregnant,
        symptoms=symptoms,
        hypotheses=hypotheses,
    )


class OpenAICaseStructureExtractor(CaseStructureExtractor):
    """Implementación de CaseStructureExtractor que usa LangChain y OpenAI para extraer la estructura del caso desde texto libre."""

    def __init__(self, *, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        if not api_key or not api_key.strip():
            raise ValueError("OPENAI_API_KEY es obligatoria para OpenAICaseStructureExtractor")
        self._model_name = model
        self._llm = ChatOpenAI(
            model=model,
            api_key=api_key.strip(),
            temperature=0,
        )

    def extract(self, text: str) -> StructuredCase:
        """Construye el prompt con el texto del caso, invoca el modelo, parsea el JSON y devuelve StructuredCase."""
        prompt = _build_extract_prompt(text)
        messages = [HumanMessage(content=prompt)]
        response = self._llm.invoke(messages)
        content = getattr(response, "content", None) or str(response)
        if not content or not content.strip():
            raise CaseStructureExtractionError("El modelo devolvió una respuesta vacía")
        data = _parse_json_from_response(content)
        return _map_json_to_structured_case(data)
