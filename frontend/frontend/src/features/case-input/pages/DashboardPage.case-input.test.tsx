import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DashboardPage } from './DashboardPage'
import { analyzeCase } from '../../../api/caseAnalysis.mock'

vi.mock('../../../api/caseAnalysis.mock', () => ({
  analyzeCase: vi.fn(),
}))

const mockAnalyzeCase = vi.mocked(analyzeCase)

describe('DashboardPage – case input section', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('disables "Analizar caso" button when textarea is empty', () => {
    render(<DashboardPage />)

    const button = screen.getByRole('button', { name: /analizar caso/i })
    expect(button).toBeDisabled()
  })

  it('calls analyzeCase with the typed text, shows loading, then shows "Información detectada del caso"', async () => {
    const user = userEvent.setup()
    const result = {
      age: 35,
      sex: 'Mujer' as const,
      isPregnant: false,
      symptoms: [{ id: '1', label: 'Dolor' }],
      hypotheses: [{ id: '1', label: 'Faringitis' }],
    }
    mockAnalyzeCase.mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve(result), 50))
    )

    render(<DashboardPage />)

    const textarea = screen.getByPlaceholderText(/mujer de 35 años/i)
    await user.type(textarea, 'Mujer 35 años con dolor de garganta')

    const button = screen.getByRole('button', { name: /analizar caso/i })
    expect(button).not.toBeDisabled()

    await user.click(button)

    expect(mockAnalyzeCase).toHaveBeenCalledWith('Mujer 35 años con dolor de garganta')

    expect(screen.getByText(/analizando/i)).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText(/información detectada del caso/i)).toBeInTheDocument()
    })
  })

  it('shows error message when analyzeCase fails', async () => {
    const user = userEvent.setup()
    mockAnalyzeCase.mockRejectedValue(new Error('Network error'))

    render(<DashboardPage />)

    const textarea = screen.getByPlaceholderText(/mujer de 35 años/i)
    await user.type(textarea, 'Texto del caso')

    const button = screen.getByRole('button', { name: /analizar caso/i })
    await user.click(button)

    await waitFor(() => {
      expect(
        screen.getByText(/no se ha podido analizar el caso/i)
      ).toBeInTheDocument()
    })
  })
})

const fullMockResponse = {
  age: 35,
  sex: 'Mujer' as const,
  isPregnant: false,
  symptoms: [
    { id: 'sym-1', label: 'Dolor de garganta' },
    { id: 'sym-2', label: 'Irritación' },
    { id: 'sym-3', label: 'Tos seca' },
  ],
  hypotheses: [
    { id: 'hyp-1', label: 'Faringitis leve' },
    { id: 'hyp-2', label: 'Irritación faríngea' },
    { id: 'hyp-3', label: 'Resfriado común' },
  ],
}

describe('DashboardPage – información detectada integration', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('after analyzing a case, shows patient data, symptoms and hypotheses blocks with initial mock values', async () => {
    const user = userEvent.setup()
    mockAnalyzeCase.mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve(fullMockResponse), 50))
    )

    render(<DashboardPage />)

    const textarea = screen.getByPlaceholderText(/mujer de 35 años/i)
    await user.type(textarea, 'Caso de prueba')
    await user.click(screen.getByRole('button', { name: /analizar caso/i }))

    await waitFor(() => {
      expect(screen.getByText(/información detectada del caso/i)).toBeInTheDocument()
    })

    expect(screen.getByRole('heading', { name: /datos del paciente/i })).toBeInTheDocument()
    expect(screen.getByLabelText(/edad/i)).toHaveValue(35)
    expect(screen.getByLabelText(/^mujer$/i)).toBeChecked()

    expect(screen.getByRole('heading', { name: /síntomas detectados/i })).toBeInTheDocument()
    expect(screen.getByText('Dolor de garganta')).toBeInTheDocument()
    expect(screen.getByText('Irritación')).toBeInTheDocument()
    expect(screen.getByText('Tos seca')).toBeInTheDocument()

    expect(screen.getByRole('heading', { name: /hipótesis clínicas orientativas/i })).toBeInTheDocument()
    expect(screen.getByText('Faringitis leve')).toBeInTheDocument()
    expect(screen.getByText('Irritación faríngea')).toBeInTheDocument()
    expect(screen.getByText('Resfriado común')).toBeInTheDocument()
  })

  it('subsection interactions update DashboardPage state', async () => {
    const user = userEvent.setup()
    mockAnalyzeCase.mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve(fullMockResponse), 50))
    )

    render(<DashboardPage />)

    await user.type(screen.getByPlaceholderText(/mujer de 35 años/i), 'Caso')
    await user.click(screen.getByRole('button', { name: /analizar caso/i }))

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /datos del paciente/i })).toBeInTheDocument()
    })

    const ageInput = screen.getByLabelText(/edad/i)
    await user.clear(ageInput)
    await user.type(ageInput, '40')
    expect(ageInput).toHaveValue(40)

    await user.click(screen.getByText('Irritación'))
    await user.click(screen.getByText('Irritación'))
    const symptomChip = screen.getByText('Irritación')
    expect(symptomChip).toBeInTheDocument()

    const addSymptomInput = screen.getByRole('textbox', { name: /añadir síntoma/i })
    await user.type(addSymptomInput, 'Fiebre')
    await user.click(screen.getByRole('button', { name: /añadir síntoma/i }))
    await waitFor(() => {
      expect(screen.getByText('Fiebre')).toBeInTheDocument()
    })
    expect(addSymptomInput).toHaveValue('')
  })
})
