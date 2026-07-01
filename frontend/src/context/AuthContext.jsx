import { createContext, useContext, useEffect, useState } from "react";

import * as authApi from "../services/auth";
import { clearToken, getToken, setToken } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  // `loading` is true while we restore a session from a stored token on refresh.
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setLoading(false);
      return;
    }
    // We have a token from a previous session — fetch the profile to confirm it.
    authApi
      .getMe()
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  async function login(credentials) {
    const { access_token } = await authApi.login(credentials);
    setToken(access_token);
    const profile = await authApi.getMe();
    setUser(profile);
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  const value = { user, loading, login, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return context;
}
