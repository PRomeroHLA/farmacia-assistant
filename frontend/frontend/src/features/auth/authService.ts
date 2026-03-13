import type { User } from '../../shared/types';

export type LoginResponse = {
  user: User;
  token?: string;
} | null;

export interface AuthService {
  login(username: string, password: string): Promise<LoginResponse>;
}

