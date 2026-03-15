import { getApiBaseUrl } from './config'
import type { StructuredCaseResponse, ProductRecommendation } from '../shared/types'

export async function getRecommendationsFromApi(
  caseData: StructuredCaseResponse
): Promise<ProductRecommendation[]> {
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
  const data = (await response.json()) as
    | ProductRecommendation[]
    | { recommendations: ProductRecommendation[]; explanation?: string }
  return Array.isArray(data) ? data : data.recommendations
}
