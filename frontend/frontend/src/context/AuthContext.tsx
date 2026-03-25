import { createContext, useState, useCallback } from 'react'
import type { ReactNode } from 'react'
import type { AuthContextValue } from './AuthContextValue'
import { login as authLogin } from '../api/auth'

export const AuthContext = createContext<AuthContextValue | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthContextValue['user']>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleLogin = useCallback(
    async (username: string, password: string) => {
      setLoading(true)
      setError(null)
      try {
        const result = await authLogin(username, password)

        if (result && result.user) {
          setUser(result.user)
          return true
        }

        setUser(null)
        setError('Credenciales inválidas')
        return false
      } catch {
        setUser(null)
        setError('No se pudo iniciar sesión. Revisa la conexión y la URL del backend.')
        return false
      } finally {
        setLoading(false)
      }
    },
    []
  )

  const handleLogout = useCallback(() => {
    setUser(null)
    setError(null)
  }, [])

  const value: AuthContextValue = {
    user,
    loading,
    error,
    login: handleLogin,
    logout: handleLogout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

