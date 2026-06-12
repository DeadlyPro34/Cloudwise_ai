/**
 * AuthContext - global authentication state.
 *
 * Provides: current user, login, register, logout, loading state.
 * Persists JWT in localStorage; rehydrates user on app load.
 */

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User, LoginPayload, RegisterPayload } from "../types";
import { getToken, setToken, clearToken } from "../services/apiClient";
import { loginUser, registerUser, getCurrentUser } from "../services/authService";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // On mount: if a token exists, fetch the current user to rehydrate session
  useEffect(() => {
    const token = getToken();
    if (!token) {
      setIsLoading(false);
      return;
    }

    getCurrentUser()
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setIsLoading(false));
  }, []);

  async function login(payload: LoginPayload) {
    const data = await loginUser(payload);
    setToken(data.access_token);
    setUser(data.user);
  }

  async function register(payload: RegisterPayload) {
    const data = await registerUser(payload);
    setToken(data.access_token);
    setUser(data.user);
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
