import { hasApiBaseUrl } from './config'
import { getRecommendationsFromApi } from './recommendations.api'
import { getRecommendations as getRecommendationsMock } from './recommendations.mock'
import type { StructuredCaseResponse, ProductRecommendation } from '../shared/types'

/**
 * Obtiene recomendaciones: usa el API real si VITE_API_BASE_URL está configurada, si no el mock.
 */
export async function getRecommendations(
  caseData: StructuredCaseResponse
): Promise<ProductRecommendation[]> {
  if (hasApiBaseUrl()) {
    return getRecommendationsFromApi(caseData)
  }
  return getRecommendationsMock(caseData)
}
