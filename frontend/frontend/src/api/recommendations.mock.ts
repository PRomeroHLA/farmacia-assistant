import type { StructuredCaseResponse, ProductRecommendation } from '../shared/types'

const MOCK_DELAY_MS = 300

const mockProducts: ProductRecommendation[] = [
  {
    id: '1',
    name: 'Strepsils Miel y Limón',
    category: 'Pastillas para la garganta',
    reason:
      'Acción antiséptica local y alivio del dolor de garganta. Eficaz en faringitis leves.',
    badge: 'main',
    price: '7.95€',
    stock: 'En stock',
    format: 'Pastillas',
  },
  {
    id: '2',
    name: 'Angileptol Spray',
    category: 'Spray bucal antiséptico',
    reason:
      'Aplicación directa sobre zona inflamada. Recomendado para irritación faríngea.',
    badge: 'alternative',
    price: '9.50€',
    stock: 'En stock',
    format: 'Spray 30ml',
  },
  {
    id: '3',
    name: 'Propóleo forte jarabe',
    category: 'Complemento natural',
    reason:
      'Efecto calmante y protector de las mucosas. Complementa tratamiento sintomático.',
    badge: 'alternative',
    price: '12.95€',
    stock: 'Pocas unidades',
    format: 'Jarabe 150ml',
  },
]

export async function getRecommendations(
  _caseData: StructuredCaseResponse
): Promise<ProductRecommendation[]> {
  await new Promise((resolve) => setTimeout(resolve, MOCK_DELAY_MS))
  return [...mockProducts]
}
