import { hasApiBaseUrl } from './config'
import { analyzeCaseFromApi } from './caseAnalysis.api'
import { analyzeCase as analyzeCaseMock } from './caseAnalysis.mock'
import type { StructuredCaseResponse } from '../shared/types'

/**
 * Analiza el texto del caso: usa el API real si VITE_API_BASE_URL está configurada, si no el mock.
 */
export async function analyzeCase(text: string): Promise<StructuredCaseResponse> {
  if (hasApiBaseUrl()) {
    return analyzeCaseFromApi(text)
  }
  return analyzeCaseMock(text)
}
