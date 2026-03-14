import { useState, type FormEvent } from 'react'
import { analyzeCase } from '../../../api/caseAnalysis.mock'
import { getRecommendations } from '../../../api/recommendations.mock'
import type {
  StructuredCaseResponse,
  Symptom,
  ClinicalHypothesis,
  ProductRecommendation,
} from '../../../shared/types'
import { CaseDescriptionSection } from '../components/CaseDescriptionSection'
import { PatientDataSection } from '../components/PatientDataSection'
import type { PatientDataValue } from '../components/PatientDataSection'
import { SymptomsSection } from '../components/SymptomsSection'
import { HypothesesSection } from '../components/HypothesesSection'

const TEXTAREA_PLACEHOLDER =
  'Ejemplo: Mujer de 35 años con dolor de garganta desde hace 3 días, sin fiebre, refiere irritación al tragar...'
const ERROR_MESSAGE =
  'No se ha podido analizar el caso. Intente de nuevo.'
const RECOMMENDATIONS_ERROR_MESSAGE =
  'No se han podido cargar las recomendaciones.'

function toPatientDataValue(data: StructuredCaseResponse): PatientDataValue {
  return {
    age: data.age !== null ? String(data.age) : '',
    sex: data.sex,
    isPregnant: data.isPregnant,
  }
}

export function DashboardPage() {
  const [caseDescription, setCaseDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [structuredCase, setStructuredCase] = useState<StructuredCaseResponse | null>(null)
  const [patientData, setPatientData] = useState<PatientDataValue | null>(null)
  const [symptoms, setSymptoms] = useState<Symptom[]>([])
  const [selectedSymptomIds, setSelectedSymptomIds] = useState<string[]>([])
  const [hypotheses, setHypotheses] = useState<ClinicalHypothesis[]>([])
  const [selectedHypothesisIds, setSelectedHypothesisIds] = useState<string[]>([])
  const [confirmed, setConfirmed] = useState(false)
  const [recommendations, setRecommendations] = useState<ProductRecommendation[]>([])
  const [loadingRecommendations, setLoadingRecommendations] = useState(false)
  const [recommendationsError, setRecommendationsError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const text = caseDescription.trim()
    if (!text) return

    setLoading(true)
    setError(null)

    try {
      const result = await analyzeCase(text)
      setStructuredCase(result)
      setPatientData(toPatientDataValue(result))
      setSymptoms(result.symptoms)
      setSelectedSymptomIds(result.symptoms.length > 0 ? result.symptoms.slice(0, 2).map((s) => s.id) : [])
      setHypotheses(result.hypotheses)
      setSelectedHypothesisIds(result.hypotheses.length > 0 ? result.hypotheses.slice(0, 2).map((h) => h.id) : [])
    } catch {
      setError(ERROR_MESSAGE)
    } finally {
      setLoading(false)
    }
  }

  const handleConfirmCase = async () => {
    if (structuredCase === null) return
    setConfirmed(true)
    setLoadingRecommendations(true)
    setRecommendationsError(null)
    try {
      const list = await getRecommendations(structuredCase)
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
  }

  const handleNewCase = () => {
    setCaseDescription('')
    setStructuredCase(null)
    setPatientData(null)
    setSymptoms([])
    setSelectedSymptomIds([])
    setHypotheses([])
    setSelectedHypothesisIds([])
    setConfirmed(false)
    setRecommendations([])
    setLoadingRecommendations(false)
    setRecommendationsError(null)
    setError(null)
    if (typeof window.scrollTo === 'function') {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <header className="sticky top-0 z-10 flex items-center justify-between border-b border-gray-200 bg-white px-4 py-3 shadow-sm">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-emerald-500" aria-hidden />
          <span className="text-lg font-semibold text-gray-800">Asistente de Recomendación Farmacéutica</span>
        </div>
        {confirmed && (
          <button
            type="button"
            onClick={handleNewCase}
            className="rounded-lg border-2 border-emerald-500 bg-white px-4 py-2 text-sm font-medium text-emerald-600 transition hover:bg-emerald-50"
          >
            Nuevo caso
          </button>
        )}
      </header>

      <div id="dashboard-content" className="mx-auto max-w-2xl px-4 py-6">
        <h1 className="text-xl font-semibold text-gray-900 mb-6">Dashboard</h1>

        <CaseDescriptionSection
          value={caseDescription}
          onChange={setCaseDescription}
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
          placeholder={TEXTAREA_PLACEHOLDER}
        />

        {structuredCase !== null && patientData !== null && (
          <section
            className="mt-6 bg-white rounded-xl border border-gray-200 p-6 shadow-sm"
            aria-labelledby="info-detectada-heading"
          >
            <h2 id="info-detectada-heading" className="text-lg font-medium text-gray-800">
              Información detectada del caso
            </h2>
            <p className="text-sm text-gray-600 mt-1 mb-6">
              Revise y confirme los datos antes de continuar
            </p>
            <PatientDataSection value={patientData} onChange={setPatientData} />
            <SymptomsSection
              symptoms={symptoms}
              selectedSymptomIds={selectedSymptomIds}
              onToggleSymptom={(id) => {
                setSelectedSymptomIds((prev) =>
                  prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
                )
              }}
              onAddSymptom={(label) => {
                const id = `sym-${symptoms.length + 1}`
                setSymptoms((prev) => [...prev, { id, label }])
                setSelectedSymptomIds((prev) => [...prev, id])
              }}
            />
            <HypothesesSection
              hypotheses={hypotheses}
              selectedHypothesisIds={selectedHypothesisIds}
              onToggleHypothesis={(id) => {
                setSelectedHypothesisIds((prev) =>
                  prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
                )
              }}
              onAddHypothesis={(label) => {
                const id = `hyp-${hypotheses.length + 1}`
                setHypotheses((prev) => [...prev, { id, label }])
                setSelectedHypothesisIds((prev) => [...prev, id])
              }}
            />
          </section>
        )}

        {structuredCase !== null && !confirmed && (
          <div className="mt-6 flex justify-center">
            <button
              type="button"
              onClick={handleConfirmCase}
              className="bg-emerald-500 hover:bg-emerald-600 text-white px-12 py-4 rounded-xl shadow-lg hover:shadow-xl font-medium transition-colors"
            >
              Confirmar caso y obtener recomendaciones
            </button>
          </div>
        )}

        {loadingRecommendations && (
          <p className="mt-6 text-center text-gray-600" role="status">
            Cargando recomendaciones...
          </p>
        )}

        {recommendationsError && (
          <p className="mt-6 text-center text-red-600" role="alert">
            {recommendationsError}
          </p>
        )}

        {recommendations.length > 0 && (
          <section id="recommendations" className="mt-8" aria-label="Recomendaciones">
            {/* Vista de recomendaciones (tarea siguiente) */}
          </section>
        )}
      </div>
    </main>
  )
}
