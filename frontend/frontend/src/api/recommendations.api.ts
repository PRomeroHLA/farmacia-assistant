import { getApiBaseUrl } from './config'
import type {
  StructuredCaseResponse,
  RecommendationSymptomGroup,
} from '../shared/types'

export async function getRecommendationsFromApi(
  caseData: StructuredCaseResponse
): Promise<RecommendationSymptomGroup[]> {
  const baseUrl = getApiBaseUrl()
  const url = `${baseUrl}/cases/recommendations`
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(caseData),
  })
  if (!response.ok) {
    throw new Error(`Recomendaciones: ${response.status} ${response.statusText}`)
  }
  const data = (await response.json()) as {
    groups: RecommendationSymptomGroup[]
    explanation?: string
  }
  return data.groups
}
