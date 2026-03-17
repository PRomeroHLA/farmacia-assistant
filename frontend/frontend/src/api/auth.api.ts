import { getApiBaseUrl } from './config'
import type { LoginResult } from '../shared/types'

export async function loginFromApi(
  username: string,
  password: string
): Promise<LoginResult> {
  const baseUrl = getApiBaseUrl()
  const url = `${baseUrl}/auth/login`

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Credenciales inválidas: el AuthContext tratará null como login fallido
      return null
    }
    throw new Error(`Login: ${response.status} ${response.statusText}`)
  }

  const data = (await response.json()) as LoginResult
  return data
}

