import type { StructuredCaseResponse } from '../shared/types'

const MOCK_DELAY_MS = 400

const mockResponse: StructuredCaseResponse = {
  age: 35,
  sex: 'Mujer',
  isPregnant: false,
  symptoms: [
    { id: 'sym-1', label: 'Dolor de garganta' },
    { id: 'sym-2', label: 'Irritación' },
    { id: 'sym-3', label: 'Tos seca' },
  ],
  hypotheses: [
    { id: 'hyp-1', label: 'Faringitis leve' },
    { id: 'hyp-2', label: 'Irritación faríngea' },
    { id: 'hyp-3', label: 'Resfriado común' },
  ],
}

export async function analyzeCase(_text: string): Promise<StructuredCaseResponse> {
  await new Promise((resolve) => setTimeout(resolve, MOCK_DELAY_MS))
  return { ...mockResponse }
}
