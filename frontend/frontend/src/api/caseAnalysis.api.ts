import { getApiBaseUrl } from './config'
import type { StructuredCaseResponse } from '../shared/types'

export async function analyzeCaseFromApi(text: string): Promise<StructuredCaseResponse> {
  const baseUrl = getApiBaseUrl()
  const url = `${baseUrl}/cases/analyze`
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
  if (!response.ok) {
    throw new Error(`Analizar caso: ${response.status} ${response.statusText}`)
  }
  const data = (await response.json()) as StructuredCaseResponse
  return data
}
