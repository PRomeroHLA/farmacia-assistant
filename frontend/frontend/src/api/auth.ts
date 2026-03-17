import type { LoginResult } from '../shared/types'
import { hasApiBaseUrl } from './config'
import { loginFromApi } from './auth.api'
import { login as loginMock } from './auth.mock'

const isTestEnv = import.meta.env.MODE === 'test'

export async function login(
  username: string,
  password: string
): Promise<LoginResult> {
  // En tests siempre usamos el mock, aunque haya API base configurada.
  if (!isTestEnv && hasApiBaseUrl()) {
    return loginFromApi(username, password)
  }
  return loginMock(username, password)
}

