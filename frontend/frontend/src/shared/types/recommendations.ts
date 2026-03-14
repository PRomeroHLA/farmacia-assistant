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
  stock?: string
  format?: string
}

/** Contrato del servicio de recomendaciones. Firma estable para mock y HTTP. */
export type GetRecommendationsFn = (
  caseData: StructuredCaseResponse
) => Promise<ProductRecommendation[]>
