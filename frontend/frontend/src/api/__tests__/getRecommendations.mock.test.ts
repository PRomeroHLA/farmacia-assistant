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
  it('returns at least one recommendation with badge "main" given valid StructuredCaseResponse', async () => {
    const result = await getRecommendations(validCaseData)
    const main = result.filter((r) => r.badge === 'main')
    expect(main.length).toBeGreaterThanOrEqual(1)
  })

  it('remaining recommendations can be badge "alternative"', async () => {
    const result = await getRecommendations(validCaseData)
    const badges = result.map((r) => r.badge)
    expect(badges.every((b) => b === 'main' || b === 'alternative')).toBe(true)
  })

  it('name, category and reason are not empty', async () => {
    const result = await getRecommendations(validCaseData)
    for (const r of result) {
      expect(r.name.trim()).not.toBe('')
      expect(r.category.trim()).not.toBe('')
      expect(r.reason.trim()).not.toBe('')
    }
  })
})
