import { describe, it, expect, vi } from 'vitest'
import { useState } from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PatientDataSection } from './PatientDataSection'
import type { PatientDataValue } from './PatientDataSection'

describe('PatientDataSection', () => {
  it('renders title "Datos del paciente"', () => {
    render(
      <PatientDataSection
        value={{ age: '35', sex: 'Mujer', isPregnant: false }}
        onChange={vi.fn()}
      />
    )
    expect(screen.getByRole('heading', { name: /datos del paciente/i })).toBeInTheDocument()
  })

  it('shows inputs for Edad, Sexo (Hombre/Mujer) and Embarazo', () => {
    render(
      <PatientDataSection
        value={{ age: '35', sex: 'Mujer', isPregnant: false }}
        onChange={vi.fn()}
      />
    )
    expect(screen.getByLabelText(/edad/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/^hombre$/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/^mujer$/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/embarazo/i)).toBeInTheDocument()
  })

  it('initializes fields with structuredCase data (age 35, sex Mujer, isPregnant false)', () => {
    render(
      <PatientDataSection
        value={{ age: '35', sex: 'Mujer', isPregnant: false }}
        onChange={vi.fn()}
      />
    )
    expect(screen.getByLabelText(/edad/i)).toHaveValue(35)
    expect(screen.getByLabelText(/^mujer$/i)).toBeChecked()
    expect(screen.getByLabelText(/^hombre$/i)).not.toBeChecked()
    expect(screen.getByLabelText(/embarazo/i)).not.toBeChecked()
  })

  it('notifies parent when Edad, Sexo and Embarazo are changed', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    function Wrapper() {
      const [value, setValue] = useState<PatientDataValue>({
        age: '35',
        sex: 'Mujer',
        isPregnant: false,
      })
      return (
        <PatientDataSection
          value={value}
          onChange={(next) => {
            setValue(next)
            onChange(next)
          }}
        />
      )
    }
    render(<Wrapper />)

    const ageInput = screen.getByLabelText(/edad/i)
    await user.clear(ageInput)
    await user.type(ageInput, '40')
    expect(onChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ age: '40', sex: 'Mujer', isPregnant: false })
    )

    await user.click(screen.getByLabelText(/^hombre$/i))
    expect(onChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ age: '40', sex: 'Hombre', isPregnant: false })
    )

    await user.click(screen.getByLabelText(/embarazo/i))
    expect(onChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ age: '40', sex: 'Hombre', isPregnant: true })
    )
  })
})
