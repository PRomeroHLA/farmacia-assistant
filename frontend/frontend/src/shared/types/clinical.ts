/**
 * Tipos para la API de análisis del caso clínico y estado estructurado en UI.
 * Usados por el mock, el cliente HTTP (tarea 07) y la UI de información del caso.
 */

export interface Symptom {
  id: string
  label: string
}

export interface ClinicalHypothesis {
  id: string
  label: string
}

/** Respuesta del backend al analizar el caso. */
export interface StructuredCaseResponse {
  age: number | null
  sex: 'Hombre' | 'Mujer' | null
  isPregnant: boolean
  symptoms: Symptom[]
  hypotheses: ClinicalHypothesis[]
}

/**
 * Estado del caso estructurado en el front: combina datos del backend
 * con campos editables por el usuario (p. ej. age como string en el input).
 */
export interface StructuredCaseState {
  age: string
  sex: 'Hombre' | 'Mujer' | null
  isPregnant: boolean
  symptoms: Symptom[]
  hypotheses: ClinicalHypothesis[]
}

/** Petición de análisis: texto libre del caso. */
export type AnalyzeCaseRequest = string

/** Aliases para compatibilidad con código existente que use los nombres anteriores. */
export type SymptomItem = Symptom
export type HypothesisItem = ClinicalHypothesis
