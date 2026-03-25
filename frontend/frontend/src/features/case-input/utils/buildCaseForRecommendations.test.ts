import { describe, it, expect } from 'vitest'
import { buildCaseForRecommendations } from './buildCaseForRecommendations'
import type { PatientDataValue } from '../components/PatientDataSection'

const patient: PatientDataValue = {
  age: '40',
  sex: 'Mujer',
  isPregnant: false,
}

describe('buildCaseForRecommendations', () => {
  it('includes only symptoms whose id is in selectedSymptomIds', () => {
    const payload = buildCaseForRecommendations(
      patient,
      [
        { id: 'a', label: 'A' },
        { id: 'b', label: 'B' },
        { id: 'c', label: 'C' },
      ],
      [],
      ['b'],
      []
    )
    expect(payload.symptoms).toEqual([{ id: 'b', label: 'B' }])
    expect(payload.hypotheses).toEqual([])
  })

  it('includes only hypotheses whose id is in selectedHypothesisIds', () => {
    const payload = buildCaseForRecommendations(
      patient,
      [],
      [
        { id: 'h1', label: 'H1' },
        { id: 'h2', label: 'H2' },
      ],
      [],
      ['h2']
    )
    expect(payload.symptoms).toEqual([])
    expect(payload.hypotheses).toEqual([{ id: 'h2', label: 'H2' }])
  })

  it('preserves list order from allSymptoms / allHypotheses', () => {
    const payload = buildCaseForRecommendations(
      patient,
      [
        { id: 'z', label: 'Z' },
        { id: 'y', label: 'Y' },
      ],
      [{ id: 'p', label: 'P' }],
      ['y', 'z'],
      ['p']
    )
    expect(payload.symptoms.map((s) => s.id)).toEqual(['z', 'y'])
    expect(payload.hypotheses.map((h) => h.id)).toEqual(['p'])
  })
})
