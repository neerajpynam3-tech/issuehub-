import axios from "axios";

// Shared axios client — every request goes through here.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

const TOKEN_KEY = "issuehub_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// Attach the Bearer token to every request when we have one.
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, the token is missing/expired: clear it and bounce to login.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearToken();
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Pull the human-readable message out of our structured error envelope.
export function getErrorMessage(error) {
  return (
    error.response?.data?.error?.message ||
    error.message ||
    "Something went wrong."
  );
}

export default api;
