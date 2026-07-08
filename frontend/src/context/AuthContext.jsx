import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { TOKEN_KEY, UNAUTHORIZED_EVENT } from "../api/client.js";
import { authApi } from "../api/endpoints.js";
import { getUsername, getUserType, isTokenExpired } from "../utils/jwt.js";

const AuthContext = createContext(null);

function readInitialToken() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token || isTokenExpired(token)) {
    localStorage.removeItem(TOKEN_KEY);
    return null;
  }
  return token;
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(readInitialToken);

  const login = useCallback((newToken) => {
    localStorage.setItem(TOKEN_KEY, newToken);
    setToken(newToken);
  }, []);

  const clearSession = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
  }, []);

  const logout = useCallback(async () => {
    const current = localStorage.getItem(TOKEN_KEY);
    if (current) {
      try {
        await authApi.logout(current);
      } catch {
        // Best-effort server logout; local session is cleared regardless.
      }
    }
    clearSession();
  }, [clearSession]);

  useEffect(() => {
    const handler = () => clearSession();
    window.addEventListener(UNAUTHORIZED_EVENT, handler);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, handler);
  }, [clearSession]);

  const value = useMemo(() => {
    const userType = token ? getUserType(token) : null;
    return {
      token,
      isAuthenticated: Boolean(token),
      isAdmin: userType === "ADMIN",
      userType,
      username: token ? getUsername(token) : null,
      login,
      logout,
    };
  }, [token, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
