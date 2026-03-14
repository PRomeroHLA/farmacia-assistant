import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DashboardPage } from '../components/DashboardPage'
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
