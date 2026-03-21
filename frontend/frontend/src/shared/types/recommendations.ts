import type { StructuredCaseResponse } from './clinical'

/**
 * Recomendación de producto devuelta por el servicio de recomendaciones.
 * Usado por el mock actual y por el cliente HTTP (tarea 07).
 */
export interface ProductRecommendation {
  id: string
  name: string
  category: string
  reason: string
  badge: 'main' | 'alternative'
  price?: string
  /** Estado de disponibilidad (p. ej. En stock). */
  stock?: string
  format?: string
  /** Síntoma o hipótesis del caso por la que se recomienda (API: recommendedFor). */
  recommendedFor?: string
  /** Margen comercial formateado (API: commercialMargin). */
  commercialMargin?: string
  /** Unidades disponibles en almacén (API: stockUnits). */
  stockUnits?: string
}

/** Grupo de recomendaciones por síntoma (orden del caso confirmado). */
export interface RecommendationSymptomGroup {
  symptomLabel: string | null
  recommendations: ProductRecommendation[]
}

/** Contrato del servicio de recomendaciones. Firma estable para mock y HTTP. */
export type GetRecommendationsFn = (
  caseData: StructuredCaseResponse
) => Promise<RecommendationSymptomGroup[]>
