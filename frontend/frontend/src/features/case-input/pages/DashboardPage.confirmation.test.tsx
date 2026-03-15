import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DashboardPage } from './DashboardPage'
import { analyzeCase } from '../../../api/caseAnalysis'
import { getRecommendations } from '../../../api/recommendations'

vi.mock('../../../api/caseAnalysis', () => ({
  analyzeCase: vi.fn(),
}))
vi.mock('../../../api/recommendations', () => ({
  getRecommendations: vi.fn(),
}))

const mockAnalyzeCase = vi.mocked(analyzeCase)
const mockGetRecommendations = vi.mocked(getRecommendations)

const structuredCaseResponse = {
  age: 35,
  sex: 'Mujer' as const,
  isPregnant: false,
  symptoms: [{ id: 'sym-1', label: 'Dolor' }],
  hypotheses: [{ id: 'hyp-1', label: 'Faringitis' }],
}

async function analyzeCaseAndWait() {
  mockAnalyzeCase.mockResolvedValue(structuredCaseResponse)
  const user = userEvent.setup()
  render(<DashboardPage />)
  await user.type(screen.getByPlaceholderText(/mujer de 35 años/i), 'Caso de prueba')
  await user.click(screen.getByRole('button', { name: /analizar caso/i }))
  await waitFor(() => {
    expect(screen.getByText(/información detectada del caso/i)).toBeInTheDocument()
  })
  return user
}

describe('DashboardPage – confirmation section', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('does not show confirm button until there is structuredCase', () => {
    render(<DashboardPage />)
    expect(
      screen.queryByRole('button', { name: /confirmar caso y obtener recomendaciones/i })
    ).not.toBeInTheDocument()
  })

  it('calls getRecommendations with structuredCase and updates state on confirm button click', async () => {
    await analyzeCaseAndWait()

    expect(
      screen.getByRole('button', { name: /confirmar caso y obtener recomendaciones/i })
    ).toBeInTheDocument()

    mockGetRecommendations.mockResolvedValue([
      {
        id: '1',
        name: 'Producto principal',
        category: 'Categoría',
        reason: 'Razón',
        badge: 'main',
      },
    ])

    await userEvent.setup().click(
      screen.getByRole('button', { name: /confirmar caso y obtener recomendaciones/i })
    )

    expect(mockGetRecommendations).toHaveBeenCalledWith(structuredCaseResponse)

    await waitFor(() => {
      expect(screen.queryByText(/cargando recomendaciones/i)).not.toBeInTheDocument()
    })
  })
})

describe('DashboardPage – Nuevo caso', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('resets to initial state when "Nuevo caso" is clicked after confirmed case with recommendations', async () => {
    mockAnalyzeCase.mockResolvedValue(structuredCaseResponse)
    mockGetRecommendations.mockResolvedValue([
      { id: '1', name: 'Producto', category: 'Cat', reason: 'Razón', badge: 'main' },
    ])
    const user = userEvent.setup()
    render(<DashboardPage />)

    await user.type(screen.getByPlaceholderText(/mujer de 35 años/i), 'Caso')
    await user.click(screen.getByRole('button', { name: /analizar caso/i }))
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /confirmar caso y obtener recomendaciones/i })).toBeInTheDocument()
    })
    await user.click(screen.getByRole('button', { name: /confirmar caso y obtener recomendaciones/i }))
    await waitFor(() => {
      expect(screen.getByText(/productos recomendados/i)).toBeInTheDocument()
    })
    expect(screen.getByRole('button', { name: /confirmar caso y obtener recomendaciones/i })).toBeInTheDocument()

    const nuevoCasoButton = screen.getByRole('button', { name: /nuevo caso/i })
    await user.click(nuevoCasoButton)

    expect(screen.getByPlaceholderText(/mujer de 35 años/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /analizar caso/i })).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/mujer de 35 años/i)).toHaveValue('')
    expect(screen.queryByText(/información detectada del caso/i)).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /confirmar caso y obtener recomendaciones/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /nuevo caso/i })).not.toBeInTheDocument()
  })
})
