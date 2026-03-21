import type { FormEvent } from 'react'

const DEFAULT_PLACEHOLDER =
  'Ejemplo: Mujer de 35 años con dolor de garganta desde hace 3 días, sin fiebre, refiere irritación al tragar...'

interface CaseDescriptionSectionProps {
  value: string
  onChange: (value: string) => void
  onSubmit: (e: FormEvent<HTMLFormElement>) => void
  loading: boolean
  error: string | null
  placeholder?: string
}

export function CaseDescriptionSection({
  value,
  onChange,
  onSubmit,
  loading,
  error,
  placeholder = DEFAULT_PLACEHOLDER,
}: CaseDescriptionSectionProps) {
  return (
    <section className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-6">
      <h2 className="text-left text-emerald-500 font-semibold mb-2">
        Descripción del caso del cliente
      </h2>
      <p className="text-left text-sm text-gray-600 mb-6">
        Describa los síntomas y condiciones del paciente
      </p>

      <form onSubmit={onSubmit}>
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full h-40 px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none"
          aria-label="Descripción del caso"
        />

        <button
          type="submit"
          disabled={!value.trim() || loading}
          className="mt-4 bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-8 py-3 rounded-lg transition-colors"
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
  )
}
