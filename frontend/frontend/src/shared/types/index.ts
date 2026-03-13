export interface User {
  id: string;
  username: string;
  fullName?: string;
}

export type LoginResult = {
  user: User;
  token?: string;
} | null;

export type LoginFn = (username: string, password: string) => Promise<LoginResult>;
