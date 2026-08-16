import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { TOKEN_STORAGE_KEY, registerUnauthorizedHandler } from '../api/client';
import * as authApi from '../api/auth';
import type { UserResponse, UserCreate, UserLogin } from '../types';

interface AuthContextValue {
  user: UserResponse | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (payload: UserLogin) => Promise<void>;
  register: (payload: UserCreate) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_STORAGE_KEY));
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const me = await authApi.getMe();
      setUser(me);
    } catch {
      logout();
    }
  }, [logout]);

  useEffect(() => {
    registerUnauthorizedHandler(() => logout());
  }, [logout]);

  useEffect(() => {
    (async () => {
      if (token) {
        await refreshUser();
      }
      setIsLoading(false);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback(async (payload: UserLogin) => {
    const { token: newToken } = await authApi.login(payload);
    localStorage.setItem(TOKEN_STORAGE_KEY, newToken);
    setToken(newToken);
    const me = await authApi.getMe();
    setUser(me);
  }, []);

  const register = useCallback(async (payload: UserCreate) => {
    await authApi.register(payload);
    // Registration doesn't automatically log the user in on the backend
    // (there's no token in the register response schema), so we chain a
    // login call using the same credentials.
    await login({ email: payload.email, password: payload.password });
  }, [login]);

  const value: AuthContextValue = {
    user,
    token,
    isLoading,
    isAuthenticated: !!token,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
