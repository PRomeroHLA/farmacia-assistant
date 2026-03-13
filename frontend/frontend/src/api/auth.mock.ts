import type { LoginFn, LoginResult } from '../shared/types'

export const login: LoginFn = async (
  username: string,
  password: string
): Promise<LoginResult> => {
  if (!username || !password) {
    return null
  }

  return {
    user: {
      id: 'mock-user-id',
      username,
      fullName: 'Usuario de prueba',
    },
    token: 'mock-token',
  }
}

