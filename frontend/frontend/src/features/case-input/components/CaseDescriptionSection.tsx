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
    <section className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <h2 className="text-lg font-medium text-gray-800 mb-1">
        Descripción del caso del cliente
      </h2>
      <p className="text-sm text-gray-600 mb-4">
        Describa los síntomas y condiciones del paciente
      </p>

      <form onSubmit={onSubmit} className="space-y-4">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full min-h-[140px] px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-y"
          aria-label="Descripción del caso"
        />

        <button
          type="submit"
          disabled={!value.trim() || loading}
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
  )
}
