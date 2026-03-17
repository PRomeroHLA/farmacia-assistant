import { hasApiBaseUrl } from './config'
import { analyzeCaseFromApi } from './caseAnalysis.api'
import { analyzeCase as analyzeCaseMock } from './caseAnalysis.mock'
import type { StructuredCaseResponse } from '../shared/types'

const isTestEnv = import.meta.env.MODE === 'test'

/**
 * Analiza el texto del caso: usa el API real si VITE_API_BASE_URL está configurada, si no el mock.
 */
export async function analyzeCase(text: string): Promise<StructuredCaseResponse> {
  // En tests siempre usamos el mock, aunque haya API base configurada.
  if (!isTestEnv && hasApiBaseUrl()) {
    return analyzeCaseFromApi(text)
  }
  return analyzeCaseMock(text)
}
