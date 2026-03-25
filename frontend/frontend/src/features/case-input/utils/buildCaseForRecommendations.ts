import type { StructuredCaseResponse } from '../../../shared/types'
import type { PatientDataValue } from '../components/PatientDataSection'

/**
 * Construye el payload para recomendaciones: solo síntomas e hipótesis marcados en la UI.
 */
export function buildCaseForRecommendations(
  patientData: PatientDataValue,
  allSymptoms: StructuredCaseResponse['symptoms'],
  allHypotheses: StructuredCaseResponse['hypotheses'],
  selectedSymptomIds: readonly string[],
  selectedHypothesisIds: readonly string[]
): StructuredCaseResponse {
  const symptomSelected = new Set(selectedSymptomIds)
  const hypothesisSelected = new Set(selectedHypothesisIds)
  const symptoms = allSymptoms.filter((s) => symptomSelected.has(s.id))
  const hypotheses = allHypotheses.filter((h) => hypothesisSelected.has(h.id))

  const ageStr = patientData.age.trim()
  const age = ageStr === '' ? null : parseInt(ageStr, 10)
  const ageValid = age !== null && !Number.isNaN(age) ? age : null
  return {
    age: ageValid,
    sex: patientData.sex,
    isPregnant: patientData.isPregnant,
    symptoms,
    hypotheses,
  }
}
