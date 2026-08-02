import axios from "axios";

export const TOKEN_KEY = "ping_token";
export const UNAUTHORIZED_EVENT = "ping:unauthorized";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const client = axios.create({
  baseURL,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    if (status === 401 || status === 403) {
      window.dispatchEvent(new CustomEvent(UNAUTHORIZED_EVENT));
    }
    return Promise.reject(error);
  },
);

export function extractError(error, fallback = "Something went wrong!") {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length) {
    const first = detail[0];
    if (first?.msg) {
      const loc = Array.isArray(first.loc) ? first.loc.slice(1).join(".") : "";
      return loc ? `${loc}: ${first.msg}` : first.msg;
    }
  }
  if (error?.message) return error.message;
  return fallback;
}

export default client;
