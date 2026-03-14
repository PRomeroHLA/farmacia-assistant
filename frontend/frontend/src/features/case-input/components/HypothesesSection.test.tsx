import { describe, it, expect, vi } from 'vitest'
import { useState } from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { HypothesesSection } from './HypothesesSection'
import type { ClinicalHypothesis } from '../../../shared/types'

const initialHypotheses: ClinicalHypothesis[] = [
  { id: 'hyp-1', label: 'Faringitis leve' },
  { id: 'hyp-2', label: 'Irritación faríngea' },
  { id: 'hyp-3', label: 'Resfriado común' },
]

describe('HypothesesSection', () => {
  it('renders initial hypotheses', () => {
    render(
      <HypothesesSection
        hypotheses={initialHypotheses}
        selectedHypothesisIds={['hyp-1']}
        onToggleHypothesis={vi.fn()}
        onAddHypothesis={vi.fn()}
      />
    )
    expect(
      screen.getByRole('heading', { name: /hipótesis clínicas orientativas/i })
    ).toBeInTheDocument()
    expect(screen.getByText('Faringitis leve')).toBeInTheDocument()
    expect(screen.getByText('Irritación faríngea')).toBeInTheDocument()
    expect(screen.getByText('Resfriado común')).toBeInTheDocument()
  })

  it('toggles selection when clicking a chip', async () => {
    const user = userEvent.setup()
    const onToggleHypothesis = vi.fn()
    render(
      <HypothesesSection
        hypotheses={initialHypotheses}
        selectedHypothesisIds={['hyp-1']}
        onToggleHypothesis={onToggleHypothesis}
        onAddHypothesis={vi.fn()}
      />
    )
    await user.click(screen.getByText('Faringitis leve'))
    expect(onToggleHypothesis).toHaveBeenCalledWith('hyp-1')
    await user.click(screen.getByText('Irritación faríngea'))
    expect(onToggleHypothesis).toHaveBeenCalledWith('hyp-2')
  })

  it('allows adding a new hypothesis that appears selected', async () => {
    const user = userEvent.setup()
    const onAddHypothesis = vi.fn()
    function Wrapper() {
      const [hypotheses, setHypotheses] = useState<ClinicalHypothesis[]>(initialHypotheses)
      const [selected, setSelected] = useState<string[]>(['hyp-1'])
      return (
        <HypothesesSection
          hypotheses={hypotheses}
          selectedHypothesisIds={selected}
          onToggleHypothesis={(id) => {
            setSelected((prev) =>
              prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
            )
          }}
          onAddHypothesis={(label) => {
            const id = `hyp-${hypotheses.length + 1}`
            setHypotheses((prev) => [...prev, { id, label }])
            setSelected((prev) => [...prev, id])
            onAddHypothesis(label)
          }}
        />
      )
    }
    render(<Wrapper />)

    const input = screen.getByRole('textbox', { name: /añadir hipótesis/i })
    await user.type(input, 'Viral')
    const addButton = screen.getByRole('button', { name: /añadir hipótesis/i })
    await user.click(addButton)

    expect(onAddHypothesis).toHaveBeenCalledWith('Viral')
    expect(screen.getByText('Viral')).toBeInTheDocument()
    expect(input).toHaveValue('')
  })
})
