import { describe, it, expect } from 'vitest'
import { getRecommendations } from '../recommendations.mock'
import type { StructuredCaseResponse } from '../../shared/types'

const validCaseData: StructuredCaseResponse = {
  age: 35,
  sex: 'Mujer',
  isPregnant: false,
  symptoms: [{ id: '1', label: 'Dolor de garganta' }],
  hypotheses: [{ id: '1', label: 'Faringitis leve' }],
}

describe('getRecommendations mock', () => {
  it('returns one group per symptom with at least one main badge', async () => {
    const groups = await getRecommendations(validCaseData)
    expect(groups.length).toBe(1)
    const mains = groups[0].recommendations.filter((r) => r.badge === 'main')
    expect(mains.length).toBeGreaterThanOrEqual(1)
  })

  it('recommendation badges are main or alternative', async () => {
    const groups = await getRecommendations(validCaseData)
    for (const g of groups) {
      for (const r of g.recommendations) {
        expect(r.badge === 'main' || r.badge === 'alternative').toBe(true)
      }
    }
  })

  it('name, category and reason are not empty', async () => {
    const groups = await getRecommendations(validCaseData)
    for (const g of groups) {
      for (const r of g.recommendations) {
        expect(r.name.trim()).not.toBe('')
        expect(r.category.trim()).not.toBe('')
        expect(r.reason.trim()).not.toBe('')
      }
    }
  })
})
