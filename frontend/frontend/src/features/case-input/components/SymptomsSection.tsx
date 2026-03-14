import { useState, type FormEvent } from 'react'
import type { Symptom } from '../../../shared/types'

interface SymptomsSectionProps {
  symptoms: Symptom[]
  selectedSymptomIds: string[]
  onToggleSymptom: (id: string) => void
  onAddSymptom: (label: string) => void
}

export function SymptomsSection({
  symptoms,
  selectedSymptomIds,
  onToggleSymptom,
  onAddSymptom,
}: SymptomsSectionProps) {
  const [newLabel, setNewLabel] = useState('')

  const handleAddSubmit = (e: FormEvent) => {
    e.preventDefault()
    const label = newLabel.trim()
    if (!label) return
    onAddSymptom(label)
    setNewLabel('')
  }

  const selectedSet = new Set(selectedSymptomIds)

  return (
    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 mt-6">
      <h3 className="text-base font-medium text-gray-800 mb-4">
        Síntomas detectados
      </h3>

      <div className="flex flex-wrap gap-2 mb-4">
        {symptoms.map((s) => {
          const selected = selectedSet.has(s.id)
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => onToggleSymptom(s.id)}
              className={
                selected
                  ? 'px-3 py-1.5 rounded-full text-sm font-medium bg-emerald-100 border-2 border-emerald-500 text-emerald-800'
                  : 'px-3 py-1.5 rounded-full text-sm font-medium bg-white border-2 border-gray-300 text-gray-700 hover:border-emerald-300'
              }
            >
              {s.label}
            </button>
          )
        })}
      </div>

      <form onSubmit={handleAddSubmit} className="flex flex-wrap items-center gap-2">
        <input
          type="text"
          value={newLabel}
          onChange={(e) => setNewLabel(e.target.value)}
          placeholder="Nuevo síntoma"
          className="flex-1 min-w-[8rem] px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
          aria-label="Añadir síntoma"
        />
        <button
          type="submit"
          className="inline-flex items-center gap-1.5 px-3 py-2 bg-emerald-500 hover:bg-emerald-600 text-white text-sm font-medium rounded-lg transition-colors"
          aria-label="Añadir síntoma"
        >
          <span aria-hidden>+</span>
          Añadir síntoma
        </button>
      </form>
    </div>
  )
}
