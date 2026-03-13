import type { User } from '../shared/types'

export interface AuthContextValue {
  user: User | null
  loading: boolean
  error: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

