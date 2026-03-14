import { describe, it, expect, vi } from 'vitest'
import { useState } from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SymptomsSection } from './SymptomsSection'
import type { Symptom } from '../../../shared/types'

const initialSymptoms: Symptom[] = [
  { id: 'sym-1', label: 'Dolor de garganta' },
  { id: 'sym-2', label: 'Irritación' },
  { id: 'sym-3', label: 'Tos seca' },
]

describe('SymptomsSection', () => {
  it('renders initial symptoms', () => {
    render(
      <SymptomsSection
        symptoms={initialSymptoms}
        selectedSymptomIds={['sym-1']}
        onToggleSymptom={vi.fn()}
        onAddSymptom={vi.fn()}
      />
    )
    expect(screen.getByRole('heading', { name: /síntomas detectados/i })).toBeInTheDocument()
    expect(screen.getByText('Dolor de garganta')).toBeInTheDocument()
    expect(screen.getByText('Irritación')).toBeInTheDocument()
    expect(screen.getByText('Tos seca')).toBeInTheDocument()
  })

  it('toggles selected state when clicking a chip', async () => {
    const user = userEvent.setup()
    const onToggleSymptom = vi.fn()
    render(
      <SymptomsSection
        symptoms={initialSymptoms}
        selectedSymptomIds={['sym-1']}
        onToggleSymptom={onToggleSymptom}
        onAddSymptom={vi.fn()}
      />
    )
    await user.click(screen.getByText('Dolor de garganta'))
    expect(onToggleSymptom).toHaveBeenCalledWith('sym-1')
    await user.click(screen.getByText('Irritación'))
    expect(onToggleSymptom).toHaveBeenCalledWith('sym-2')
  })

  it('adds new symptom, selects it and clears input when submitting "Añadir síntoma"', async () => {
    const user = userEvent.setup()
    const onAddSymptom = vi.fn()
    function Wrapper() {
      const [symptoms, setSymptoms] = useState<Symptom[]>(initialSymptoms)
      const [selected, setSelected] = useState<string[]>(['sym-1'])
      return (
        <SymptomsSection
          symptoms={symptoms}
          selectedSymptomIds={selected}
          onToggleSymptom={(id) => {
            setSelected((prev) =>
              prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
            )
          }}
          onAddSymptom={(label) => {
            const id = `sym-${symptoms.length + 1}`
            setSymptoms((prev) => [...prev, { id, label }])
            setSelected((prev) => [...prev, id])
            onAddSymptom(label)
          }}
        />
      )
    }
    render(<Wrapper />)

    const input = screen.getByRole('textbox', { name: /añadir síntoma/i })
    await user.type(input, 'Fiebre')
    expect(input).toHaveValue('Fiebre')

    const addButton = screen.getByRole('button', { name: /añadir síntoma/i })
    await user.click(addButton)

    expect(onAddSymptom).toHaveBeenCalledWith('Fiebre')
    expect(screen.getByText('Fiebre')).toBeInTheDocument()
    expect(input).toHaveValue('')
  })
})
