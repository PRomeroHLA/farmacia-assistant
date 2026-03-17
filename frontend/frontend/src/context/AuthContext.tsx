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

      const result = await authLogin(username, password)

      if (result && result.user) {
        setUser(result.user)
      } else {
        setUser(null)
        setError('Invalid credentials')
      }

      setLoading(false)
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

