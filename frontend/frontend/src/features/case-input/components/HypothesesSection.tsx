import { useState, type FormEvent } from 'react'
import type { ClinicalHypothesis } from '../../../shared/types'

interface HypothesesSectionProps {
  hypotheses: ClinicalHypothesis[]
  selectedHypothesisIds: string[]
  onToggleHypothesis: (id: string) => void
  onAddHypothesis: (label: string) => void
}

export function HypothesesSection({
  hypotheses,
  selectedHypothesisIds,
  onToggleHypothesis,
  onAddHypothesis,
}: HypothesesSectionProps) {
  const [newLabel, setNewLabel] = useState('')

  const handleAddSubmit = (e: FormEvent) => {
    e.preventDefault()
    const label = newLabel.trim()
    if (!label) return
    onAddHypothesis(label)
    setNewLabel('')
  }

  const selectedSet = new Set(selectedHypothesisIds)

  return (
    <div className="bg-gray-50 rounded-lg p-6">
      <h3 className="text-left text-gray-800 mb-2">
        Hipótesis clínicas orientativas
      </h3>
      <p className="text-left text-sm text-gray-500 mb-4">
        Opcional - para referencia clínica
      </p>

      <div className="flex flex-wrap gap-2 mb-4">
        {hypotheses.map((h) => {
          const selected = selectedSet.has(h.id)
          return (
            <button
              key={h.id}
              type="button"
              onClick={() => onToggleHypothesis(h.id)}
              className={`px-4 py-2 rounded-full border-2 transition-all ${
                selected
                  ? 'bg-emerald-500 border-emerald-500 text-white'
                  : 'bg-white border-gray-200 text-gray-700 hover:border-emerald-300'
              }`}
            >
              {h.label}
            </button>
          )
        })}
      </div>

      <form onSubmit={handleAddSubmit} className="flex gap-2">
        <input
          type="text"
          value={newLabel}
          onChange={(e) => setNewLabel(e.target.value)}
          placeholder="Nueva hipótesis..."
          className="flex-1 px-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
          aria-label="Añadir hipótesis"
        />
        <button
          type="submit"
          className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg transition-colors"
          aria-label="Añadir hipótesis"
        >
          <span aria-hidden>+</span>
          Añadir hipótesis
        </button>
      </form>
    </div>
  )
}
