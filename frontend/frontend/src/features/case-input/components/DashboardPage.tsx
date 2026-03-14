import { useState, type FormEvent } from 'react'
import { analyzeCase } from '../../../api/caseAnalysis.mock'
import type { StructuredCaseResponse, Symptom, ClinicalHypothesis } from '../../../shared/types'
import { PatientDataSection } from './PatientDataSection'
import type { PatientDataValue } from './PatientDataSection'
import { SymptomsSection } from './SymptomsSection'
import { HypothesesSection } from './HypothesesSection'

const TEXTAREA_PLACEHOLDER =
  'Ejemplo: Mujer de 35 años con dolor de garganta desde hace 3 días, sin fiebre, refiere irritación al tragar...'
const ERROR_MESSAGE =
  'No se ha podido analizar el caso. Intente de nuevo.'

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

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-6">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-xl font-semibold text-gray-900 mb-6">Dashboard</h1>

        <section className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h2 className="text-lg font-medium text-gray-800 mb-1">
            Descripción del caso del cliente
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            Describa los síntomas y condiciones del paciente
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <textarea
              value={caseDescription}
              onChange={(e) => setCaseDescription(e.target.value)}
              placeholder={TEXTAREA_PLACEHOLDER}
              className="w-full min-h-[140px] px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-y"
              aria-label="Descripción del caso"
            />

            <button
              type="submit"
              disabled={!caseDescription.trim() || loading}
              className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-colors"
            >
              {loading ? 'Analizando...' : 'Analizar caso'}
            </button>

            {error && (
              <p className="text-sm text-red-600" role="alert">
                {error}
              </p>
            )}
          </form>
        </section>

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
      </div>
    </main>
  )
}
