import { useState, useCallback } from 'react'
import { getRecommendations } from '../../../api/recommendations.mock'
import type { StructuredCaseResponse, ProductRecommendation } from '../../../shared/types'

const RECOMMENDATIONS_ERROR_MESSAGE =
  'No se han podido cargar las recomendaciones.'

export function useRecommendationsState() {
  const [confirmed, setConfirmed] = useState(false)
  const [recommendations, setRecommendations] = useState<ProductRecommendation[]>([])
  const [loadingRecommendations, setLoadingRecommendations] = useState(false)
  const [recommendationsError, setRecommendationsError] = useState<string | null>(null)

  const confirmCase = useCallback(async (caseData: StructuredCaseResponse) => {
    setConfirmed(true)
    setLoadingRecommendations(true)
    setRecommendationsError(null)
    try {
      const list = await getRecommendations(caseData)
      setRecommendations(list)
      setLoadingRecommendations(false)
      setTimeout(() => {
        const el = document.getElementById('recommendations')
        if (el && typeof el.scrollIntoView === 'function') {
          el.scrollIntoView({ behavior: 'smooth' })
        }
      }, 100)
    } catch {
      setRecommendationsError(RECOMMENDATIONS_ERROR_MESSAGE)
      setLoadingRecommendations(false)
    }
  }, [])

  const reset = useCallback(() => {
    setConfirmed(false)
    setRecommendations([])
    setLoadingRecommendations(false)
    setRecommendationsError(null)
  }, [])

  return {
    confirmed,
    recommendations,
    loadingRecommendations,
    recommendationsError,
    confirmCase,
    reset,
  }
}
