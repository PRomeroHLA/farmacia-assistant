import { afterEach, describe, expect, it, vi } from 'vitest'
import { getApiBaseUrl } from './config'

describe('api config', () => {
  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it('removes trailing slash from VITE_API_BASE_URL', () => {
    vi.stubEnv('VITE_API_BASE_URL', 'https://backend.example.com/')

    expect(getApiBaseUrl()).toBe('https://backend.example.com')
  })
})
