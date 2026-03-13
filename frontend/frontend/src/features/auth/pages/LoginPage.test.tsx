import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginPage } from '../LoginPage'
import { AuthProvider } from '../../../context/AuthContext'

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>(
    'react-router-dom'
  )
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  }
})

const renderWithProviders = () =>
  render(
    <AuthProvider>
      <LoginPage />
    </AuthProvider>
  )

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders username, password fields and "Iniciar sesión" button', () => {
    renderWithProviders()

    expect(
      screen.getByLabelText(/usuario/i)
    ).toBeInTheDocument()
    expect(
      screen.getByLabelText(/contraseña/i)
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /iniciar sesión/i })
    ).toBeInTheDocument()
  })
})

