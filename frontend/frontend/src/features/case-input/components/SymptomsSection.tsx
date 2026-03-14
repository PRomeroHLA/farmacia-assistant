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
    <div className="bg-gray-50 rounded-lg p-6 mb-6">
      <h3 className="text-left text-gray-800 mb-4">
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
              className={`px-4 py-2 rounded-full border-2 transition-all ${
                selected
                  ? 'bg-emerald-500 border-emerald-500 text-white'
                  : 'bg-white border-gray-200 text-gray-700 hover:border-emerald-300'
              }`}
            >
              {s.label}
            </button>
          )
        })}
      </div>

      <form onSubmit={handleAddSubmit} className="flex gap-2">
        <input
          type="text"
          value={newLabel}
          onChange={(e) => setNewLabel(e.target.value)}
          placeholder="Nuevo síntoma..."
          className="flex-1 px-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
          aria-label="Añadir síntoma"
        />
        <button
          type="submit"
          className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg transition-colors"
          aria-label="Añadir síntoma"
        >
          <span aria-hidden>+</span>
          Añadir síntoma
        </button>
      </form>
    </div>
  )
}
