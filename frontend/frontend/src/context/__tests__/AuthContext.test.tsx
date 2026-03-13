import { describe, it, expect } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { AuthProvider } from '../AuthContext'
import { useAuth } from '../useAuth'
import type React from 'react'

const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AuthProvider>{children}</AuthProvider>
)

describe('AuthContext / useAuth', () => {
  it('login(username, password) updates user with the user returned by the mock', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper })

    await act(async () => {
      await result.current.login('pharmacist', 'secure-password')
    })

    expect(result.current.user).not.toBeNull()
    expect(result.current.user?.username).toBe('pharmacist')
  })

  it('logout() clears user', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper })

    await act(async () => {
      await result.current.login('pharmacist', 'secure-password')
    })
    expect(result.current.user).not.toBeNull()

    act(() => {
      result.current.logout()
    })

    expect(result.current.user).toBeNull()
  })

  it('manages loading and error during login', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper })

    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBeNull()

    await act(async () => {
      await result.current.login('', '')
    })

    expect(result.current.loading).toBe(false)
    expect(result.current.user).toBeNull()
    expect(result.current.error).not.toBeNull()
  })
})

