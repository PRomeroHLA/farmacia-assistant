import { hasApiBaseUrl } from './config'
import { getRecommendationsFromApi } from './recommendations.api'
import { getRecommendations as getRecommendationsMock } from './recommendations.mock'
import type {
  StructuredCaseResponse,
  RecommendationSymptomGroup,
} from '../shared/types'

const isTestEnv = import.meta.env.MODE === 'test'

/**
 * Obtiene recomendaciones: usa el API real si VITE_API_BASE_URL está configurada, si no el mock.
 */
export async function getRecommendations(
  caseData: StructuredCaseResponse
): Promise<RecommendationSymptomGroup[]> {
  // En tests siempre usamos el mock, aunque haya API base configurada.
  if (!isTestEnv && hasApiBaseUrl()) {
    return getRecommendationsFromApi(caseData)
  }
  return getRecommendationsMock(caseData)
}
