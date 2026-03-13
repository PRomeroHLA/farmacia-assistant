import { describe, it, expect } from 'vitest'
import { login } from './auth.mock'

describe('auth.mock login', () => {
  it('returns a user and optional token when username and password are not empty', async () => {
    const result = await login('pharmacist', 'secure-password')

    expect(result).not.toBeNull()
    if (!result) return

    expect(result.user).toBeDefined()
    expect(result.user.username).toBe('pharmacist')
  })

  it('returns null when username is empty', async () => {
    const result = await login('', 'secure-password')
    expect(result).toBeNull()
  })

  it('returns null when password is empty', async () => {
    const result = await login('pharmacist', '')
    expect(result).toBeNull()
  })
})

