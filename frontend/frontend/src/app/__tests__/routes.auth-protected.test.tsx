import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext, AuthProvider } from '../../context/AuthContext'
import type { AuthContextValue } from '../../context/AuthContextValue'
import { AppRoutes } from '../routes'
import { DashboardPage } from '../../features/auth/DashboardPage'

describe('Protected routes', () => {
  it('redirects to /login when accessing /dashboard without an authenticated user', () => {
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </MemoryRouter>
    )

    expect(
      screen.getByRole('heading', {
        name: /asistente de recomendación farmacéutica/i,
      })
    ).toBeInTheDocument()
  })

  it('renders DashboardPage when there is an authenticated user', () => {
    const mockValue: AuthContextValue = {
      user: {
        id: 'user-1',
        username: 'pharmacist',
        fullName: 'Usuario Farmacéutico',
      },
      loading: false,
      error: null,
      login: async () => {},
      logout: () => {},
    }

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <AuthContext.Provider value={mockValue}>
          <DashboardPage />
        </AuthContext.Provider>
      </MemoryRouter>
    )

    expect(
      screen.getByRole('heading', { name: /dashboard/i })
    ).toBeInTheDocument()
  })
})

