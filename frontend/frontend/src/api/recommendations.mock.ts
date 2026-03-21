import type {
  StructuredCaseResponse,
  ProductRecommendation,
  RecommendationSymptomGroup,
} from '../shared/types'

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
    recommendedFor: 'Dolor de garganta',
    commercialMargin: '2,10 €',
    stockUnits: '63',
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
    recommendedFor: 'Odinofagia (dolor al tragar)',
    commercialMargin: '1,85 €',
    stockUnits: '22',
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
    recommendedFor: 'Tos seca',
    commercialMargin: '3,20 €',
    stockUnits: '4',
  },
]

function withBadges(products: ProductRecommendation[]): ProductRecommendation[] {
  return products.map((p, i) => ({
    ...p,
    badge: i === 0 ? ('main' as const) : ('alternative' as const),
  }))
}

function sliceForSymptom(
  label: string,
  offset: number
): ProductRecommendation[] {
  const rotated = [
    mockProducts[offset % mockProducts.length],
    mockProducts[(offset + 1) % mockProducts.length],
    mockProducts[(offset + 2) % mockProducts.length],
  ]
  return withBadges(
    rotated.map((p) => ({
      ...p,
      recommendedFor: label,
    }))
  )
}

export async function getRecommendations(
  caseData: StructuredCaseResponse
): Promise<RecommendationSymptomGroup[]> {
  await new Promise((resolve) => setTimeout(resolve, MOCK_DELAY_MS))

  if (caseData.symptoms.length > 0) {
    return caseData.symptoms.map((s, index) => ({
      symptomLabel: s.label,
      recommendations: sliceForSymptom(s.label, index),
    }))
  }

  return [
    {
      symptomLabel: null,
      recommendations: withBadges(mockProducts.map((p) => ({ ...p }))),
    },
  ]
}
