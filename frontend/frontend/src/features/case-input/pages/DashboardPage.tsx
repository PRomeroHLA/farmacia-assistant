import type { StructuredCaseResponse } from '../../../shared/types'
import { useCaseInputState } from '../hooks/useCaseInputState'
import { useRecommendationsState } from '../../recommendations'
import { CaseDescriptionSection } from '../components/CaseDescriptionSection'
import { PatientDataSection } from '../components/PatientDataSection'
import type { PatientDataValue } from '../components/PatientDataSection'
import { SymptomsSection } from '../components/SymptomsSection'
import { HypothesesSection } from '../components/HypothesesSection'
import { RecommendationCard } from '../../recommendations'

function buildCaseForRecommendations(
  patientData: PatientDataValue,
  symptoms: StructuredCaseResponse['symptoms'],
  hypotheses: StructuredCaseResponse['hypotheses']
): StructuredCaseResponse {
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

export function DashboardPage() {
  const caseInput = useCaseInputState()
  const recs = useRecommendationsState()

  const {
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
    reset: resetCaseInput,
  } = caseInput

  const {
    confirmed,
    recommendations,
    loadingRecommendations,
    recommendationsError,
    confirmCase,
    reset: resetRecommendations,
  } = recs

  const handleNewCase = () => {
    resetCaseInput()
    resetRecommendations()
    if (typeof window.scrollTo === 'function') {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handleConfirmCase = () => {
    if (structuredCase !== null && patientData !== null) {
      const caseData = buildCaseForRecommendations(patientData, symptoms, hypotheses)
      confirmCase(caseData)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-500 p-2 rounded-lg flex items-center justify-center" aria-hidden>
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                viewBox="0 0 24 24"
                aria-hidden
              >
                <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
              </svg>
            </div>
            <div>
              <h1 className="text-emerald-500 font-semibold text-lg">Asistente Farmacéutico</h1>
              <p className="text-sm text-gray-500">Sistema de recomendación de productos</p>
            </div>
          </div>
          {confirmed && (
            <button
              type="button"
              onClick={handleNewCase}
              className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg transition-colors whitespace-nowrap"
            >
              Nuevo caso
            </button>
          )}
        </div>
      </header>

      <main id="dashboard-content" className="max-w-6xl mx-auto px-6 py-8">
        <CaseDescriptionSection
          value={caseDescription}
          onChange={setCaseDescription}
          onSubmit={handleSubmit}
          loading={loadingAnalyze}
          error={analyzeError}
        />

        {structuredCase !== null && patientData !== null && (
          <section
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-6"
            aria-labelledby="info-detectada-heading"
          >
            <h2 id="info-detectada-heading" className="text-left text-gray-800 mb-1">
              Información detectada del caso
            </h2>
            <p className="text-left text-sm text-gray-600 mb-6">
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

        {structuredCase !== null && patientData !== null && (
          <section className="mb-6 flex justify-center">
            <button
              type="button"
              onClick={handleConfirmCase}
              disabled={loadingRecommendations}
              className="bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-12 py-4 rounded-xl transition-colors shadow-lg hover:shadow-xl"
            >
              Confirmar caso y obtener recomendaciones
            </button>
          </section>
        )}

        {loadingRecommendations && (
          <p className="mb-6 text-center text-gray-600" role="status">
            Cargando recomendaciones...
          </p>
        )}

        {recommendationsError && (
          <p className="mb-6 text-center text-red-600" role="alert">
            {recommendationsError}
          </p>
        )}

        {recommendations.length > 0 && (
          <section
            id="recommendations"
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
            aria-label="Recomendaciones"
          >
            <h2 className="text-left text-gray-800 mb-1">Productos recomendados</h2>
            <p className="text-left text-sm text-gray-600 mb-6">
              Basado en el caso validado y disponibilidad en stock
            </p>

            <ul className="space-y-4" aria-label="Lista de productos recomendados">
              {recommendations.map((product) => (
                <li key={product.id}>
                  <RecommendationCard product={product} />
                </li>
              ))}
            </ul>
          </section>
        )}
      </main>
    </div>
  )
}

