import { useState, useCallback, type FormEvent } from 'react'
import { analyzeCase } from '../../../api/caseAnalysis.mock'
import type {
  StructuredCaseResponse,
  Symptom,
  ClinicalHypothesis,
} from '../../../shared/types'
import type { PatientDataValue } from '../components/PatientDataSection'

const ERROR_MESSAGE =
  'No se ha podido analizar el caso. Intente de nuevo.'

function toPatientDataValue(data: StructuredCaseResponse): PatientDataValue {
  return {
    age: data.age !== null ? String(data.age) : '',
    sex: data.sex,
    isPregnant: data.isPregnant,
  }
}

export function useCaseInputState() {
  const [caseDescription, setCaseDescription] = useState('')
  const [loadingAnalyze, setLoadingAnalyze] = useState(false)
  const [analyzeError, setAnalyzeError] = useState<string | null>(null)
  const [structuredCase, setStructuredCase] = useState<StructuredCaseResponse | null>(null)
  const [patientData, setPatientData] = useState<PatientDataValue | null>(null)
  const [symptoms, setSymptoms] = useState<Symptom[]>([])
  const [selectedSymptomIds, setSelectedSymptomIds] = useState<string[]>([])
  const [hypotheses, setHypotheses] = useState<ClinicalHypothesis[]>([])
  const [selectedHypothesisIds, setSelectedHypothesisIds] = useState<string[]>([])

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault()
    const text = caseDescription.trim()
    if (!text) return

    setLoadingAnalyze(true)
    setAnalyzeError(null)

    try {
      const result = await analyzeCase(text)
      setStructuredCase(result)
      setPatientData(toPatientDataValue(result))
      setSymptoms(result.symptoms)
      setSelectedSymptomIds(
        result.symptoms.length > 0
          ? result.symptoms.slice(0, 2).map((s) => s.id)
          : []
      )
      setHypotheses(result.hypotheses)
      setSelectedHypothesisIds(
        result.hypotheses.length > 0
          ? result.hypotheses.slice(0, 2).map((h) => h.id)
          : []
      )
    } catch {
      setAnalyzeError(ERROR_MESSAGE)
    } finally {
      setLoadingAnalyze(false)
    }
  }, [caseDescription])

  const reset = useCallback(() => {
    setCaseDescription('')
    setLoadingAnalyze(false)
    setAnalyzeError(null)
    setStructuredCase(null)
    setPatientData(null)
    setSymptoms([])
    setSelectedSymptomIds([])
    setHypotheses([])
    setSelectedHypothesisIds([])
  }, [])

  return {
    caseDescription,
    setCaseDescription,
    loadingAnalyze,
    analyzeError,
    structuredCase,
    patientData,
    setPatientData,
    symptoms,
    setSymptoms,
    selectedSymptomIds,
    setSelectedSymptomIds,
    hypotheses,
    setHypotheses,
    selectedHypothesisIds,
    setSelectedHypothesisIds,
    handleSubmit,
    reset,
  }
}
