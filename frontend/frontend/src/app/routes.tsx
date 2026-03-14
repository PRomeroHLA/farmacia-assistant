import { Routes, Route, Navigate } from 'react-router-dom'
import { LoginPage } from '../features/auth/LoginPage'
import { DashboardPage } from '../features/auth/DashboardPage'

/**
 * Configuración de rutas del frontend.
 * - "/" redirige a "/login"
 * - "/login" → LoginPage (feature auth)
 * - "/dashboard" → DashboardPage protegida por AuthContext (redirige a login si no hay usuario)
 *
 * Debe renderizarse dentro de AuthProvider y de un Router (BrowserRouter o MemoryRouter).
 */
export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
    </Routes>
  )
}
