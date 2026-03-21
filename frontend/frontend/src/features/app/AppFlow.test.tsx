import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { AuthProvider } from '../../context/AuthContext'
import { AppRoutes } from '../../app/routes'

vi.mock('../../api/caseAnalysis', () => ({
  analyzeCase: vi.fn().mockResolvedValue({
    age: 35,
    sex: 'Mujer' as const,
    isPregnant: false,
    symptoms: [{ id: 'sym-1', label: 'Dolor de garganta' }],
    hypotheses: [{ id: 'hyp-1', label: 'Faringitis leve' }],
  }),
}))

vi.mock('../../api/recommendations', () => ({
  getRecommendations: vi.fn().mockResolvedValue([
    {
      symptomLabel: 'Dolor de garganta',
      recommendations: [
        { id: '1', name: 'Producto A', category: 'Cat', reason: 'Razón', badge: 'main' as const },
        { id: '2', name: 'Producto B', category: 'Cat', reason: 'Razón', badge: 'alternative' as const },
      ],
    },
  ]),
}))

/**
 * Test de integración de alto nivel: flujo completo desde login
 * hasta visualización de productos recomendados y "Nuevo caso".
 * Mockea caseAnalysis y getRecommendations para no depender de env ni red.
 */
function renderApp(initialRoute = '/login') {
  return render(
    <MemoryRouter initialEntries={[initialRoute]}>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </MemoryRouter>
  )
}

describe('AppFlow – flujo completo login → recomendaciones → nuevo caso', () => {
  it('completa login, análisis de caso, confirmación, recomendaciones y nuevo caso', async () => {
    const user = userEvent.setup()
    renderApp('/login')

    // 1) Login
    await user.type(screen.getByLabelText(/usuario/i), 'pharmacist')
    await user.type(screen.getByLabelText(/contraseña/i), 'password')
    await user.click(screen.getByRole('button', { name: /iniciar sesión/i }))

    // 2) Esperar navegación a dashboard
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /descripción del caso del cliente/i })).toBeInTheDocument()
    })

    // 3) Rellenar caso y analizar
    const textarea = screen.getByRole('textbox', { name: /descripción del caso/i })
    await user.type(textarea, 'Mujer de 35 años con dolor de garganta')
    await user.click(screen.getByRole('button', { name: /analizar caso/i }))

    // 4) Esperar "Información detectada del caso" y verificar datos
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /información detectada del caso/i })).toBeInTheDocument()
    })
    expect(screen.getByText(/datos del paciente/i)).toBeInTheDocument()
    expect(screen.getByText(/síntomas detectados/i)).toBeInTheDocument()
    expect(screen.getByText(/hipótesis clínicas orientativas/i)).toBeInTheDocument()

    // 5) Confirmar caso y obtener recomendaciones
    await user.click(screen.getByRole('button', { name: /confirmar caso y obtener recomendaciones/i }))

    // 6) Esperar sección "Productos recomendados" y tarjetas (al menos una principal y alguna alternativa)
    await waitFor(
      () => {
        expect(screen.getByRole('heading', { name: /productos recomendados/i })).toBeInTheDocument()
        expect(screen.getByText('Recomendación principal')).toBeInTheDocument()
        expect(screen.getAllByText('Alternativa').length).toBeGreaterThanOrEqual(1)
      },
      { timeout: 3000 }
    )

    // 7) Nuevo caso: verificar que se vuelve al estado inicial del dashboard
    await user.click(screen.getByRole('button', { name: /nuevo caso/i }))

    await waitFor(() => {
      // Sin "Información detectada" visible
      expect(screen.queryByRole('heading', { name: /información detectada del caso/i })).not.toBeInTheDocument()
      // Sin "Productos recomendados"
      expect(screen.queryByRole('heading', { name: /productos recomendados/i })).not.toBeInTheDocument()
      // Sin botón "Nuevo caso" (solo visible cuando confirmed)
      expect(screen.queryByRole('button', { name: /nuevo caso/i })).not.toBeInTheDocument()
      // Contenido del dashboard visible (descripción del caso)
      expect(screen.getByRole('heading', { name: /descripción del caso del cliente/i })).toBeInTheDocument()
    })
  }, 15000)
})
